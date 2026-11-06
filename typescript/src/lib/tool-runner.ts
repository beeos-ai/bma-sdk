// Custom tools (ADR 0012 D7). A BMA custom tool call stays `ready` until a
// consumer submits its result (`submitToolCallResult`); this module gives
// that consumer a typed shape, after @anthropic-ai/sdk's
// betaStandardSchemaTool / betaZodTool and sessions.events.toolRunner.
import type { RequestOptions } from "../core.js";
import { BmaError, ConflictError } from "../errors.js";
import type {
  AgentConfigDefinitionTool,
  SubmitToolResultContentBlock,
  ToolCall,
  ToolCallEnvelope,
} from "../generated/rest-types.js";
import { OP, type StreamEventsEvent } from "../generated/rest-operations.js";
import type { ListToolCallsResponse } from "../generated/rest-types.js";
import { APIResource } from "../resource.js";

/** The Standard Schema v1 interface (https://standardschema.dev), as published. */
export interface StandardSchemaV1<Input = unknown, Output = Input> {
  readonly "~standard": {
    readonly version: 1;
    readonly vendor: string;
    readonly validate: (value: unknown) => StandardResult<Output> | Promise<StandardResult<Output>>;
    readonly types?: { readonly input: Input; readonly output: Output } | undefined;
    /** Standard JSON Schema (zod >= 4.2, valibot via toStandardJsonSchema). */
    readonly jsonSchema?: { readonly input: (options: { target: string }) => Record<string, unknown> };
  };
}
type StandardResult<Output> =
  | { readonly value: Output; readonly issues?: undefined }
  | { readonly issues: ReadonlyArray<{ readonly message: string; readonly path?: ReadonlyArray<PropertyKey | { key: PropertyKey }> }> };
type InferOutput<S extends StandardSchemaV1> = NonNullable<S["~standard"]["types"]>["output"];

/** What a tool returns: text, or result content blocks. */
export type ToolOutput = string | SubmitToolResultContentBlock[];

/** Throw from `run` to report a failed call with this content to the model. */
export class ToolError extends Error {
  readonly content: ToolOutput;
  constructor(content: ToolOutput) {
    super(typeof content === "string" ? content : "tool error");
    this.name = "ToolError";
    this.content = content;
  }
}

export interface ToolRunContext {
  toolCall: ToolCall;
  signal: AbortSignal;
}

export interface RunnableTool<Input = unknown> {
  readonly name: string;
  /** Agent config entry for `tools.<name>`. */
  readonly definition: AgentConfigDefinitionTool & { type: "custom"; description: string };
  parse(input: unknown): Promise<Input>;
  run(input: Input, context: ToolRunContext): ToolOutput | Promise<ToolOutput>;
}

/**
 * Defines a custom tool from a Standard Schema (zod, valibot, arktype). The
 * input is validated before `run` sees it; the JSON Schema for the agent
 * config comes from the schema's Standard JSON Schema or `jsonSchema`.
 */
export function defineTool<S extends StandardSchemaV1>(options: {
  name: string;
  description: string;
  inputSchema: S;
  /** JSON Schema of the input; derived from `inputSchema` when omitted. */
  jsonSchema?: Record<string, unknown>;
  run: (input: InferOutput<S>, context: ToolRunContext) => ToolOutput | Promise<ToolOutput>;
}): RunnableTool<InferOutput<S>> {
  const std = options.inputSchema["~standard"];
  const schema = options.jsonSchema ?? std.jsonSchema?.input({ target: "draft-2020-12" });
  if (!schema) {
    throw new BmaError(
      `bma: cannot derive a JSON Schema from this ${std.vendor} schema; pass jsonSchema or use a library implementing Standard JSON Schema (zod >= 4.2)`,
    );
  }
  if (schema.type !== "object") throw new BmaError(`bma: input schema of tool ${options.name} must be an object`);
  return {
    name: options.name,
    definition: {
      type: "custom",
      description: options.description,
      input_schema: schema as AgentConfigDefinitionTool["input_schema"] & object,
    },
    async parse(input) {
      const result = await std.validate(input);
      if (result.issues) {
        const detail = result.issues
          .slice(0, 5)
          .map((i) => {
            const path = (i.path ?? []).map((p) => String(typeof p === "object" ? p.key : p)).join(".");
            return path ? `${path}: ${i.message}` : i.message;
          })
          .join("; ");
        throw new ToolError(`invalid input for ${options.name}: ${detail}`);
      }
      return result.value as InferOutput<S>;
    },
    run: options.run,
  };
}

export interface ToolRunnerParams {
  /** Only calls made in this session (calls of subagents are always handled). */
  session_id?: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  tools: RunnableTool<any>[];
  org_id?: string;
  project_id?: string;
  /**
   * Event stream reconnects in a row that receive no data before the runner
   * fails; unlimited by default (with backoff up to 8 s), so a runner rides
   * out deployments. Independent of `maxRetries`, which bounds each request.
   */
  max_reconnects?: number;
}

/** A running tool consumer. */
export interface ToolRunner {
  /** Resolves when the runner stops; rejects with the error that stopped it. */
  done(): Promise<void>;
  /** Stops listening and waits for running tools to finish. */
  stop(): Promise<void>;
}

export class ToolCallsBase extends APIResource {
  /**
   * Runs custom tools for an agent: every `ready` custom call (of the agent
   * and its subagents) whose name matches a tool is parsed, run, and its
   * result submitted. Ready calls are listed on every (re)connection of the
   * event stream, so calls that became ready while disconnected are not lost.
   * A 409 on submit (another consumer answered the call first) counts as
   * handled. `done()` rejects only with the error that stopped the runner.
   */
  runner(agentId: string, params: ToolRunnerParams, options?: RequestOptions): ToolRunner {
    const tools = new Map(params.tools.map((t) => [t.name, t]));
    if (tools.size !== params.tools.length) throw new BmaError("bma: tool names must be unique");
    const scope = { org_id: params.org_id, project_id: params.project_id };
    const controller = new AbortController();
    options?.signal?.addEventListener("abort", () => controller.abort(), { once: true });
    // Calls being run or submitted; a call leaves the set once its result is
    // stored, after which the server no longer reports it as ready.
    const inFlight = new Set<string>();
    const running = new Set<Promise<void>>();
    let failure: unknown;
    const fail = (error: unknown) => {
      failure ??= error;
      controller.abort();
    };

    const handle = (call: ToolCall) => {
      const tool = tools.get(call.name);
      if (call.type !== "custom" || call.state !== "ready" || !tool || inFlight.has(call.id)) return;
      if (params.session_id && call.agent_id === agentId && call.session_id !== params.session_id) return;
      inFlight.add(call.id);
      const task = (async () => {
        let outcome: "succeeded" | "failed" = "succeeded";
        let output: ToolOutput;
        try {
          output = await tool.run(await tool.parse(call.input), { toolCall: call, signal: controller.signal });
        } catch (error) {
          outcome = "failed";
          output = error instanceof ToolError ? error.content : error instanceof Error ? error.message : String(error);
        }
        const content_blocks: SubmitToolResultContentBlock[] =
          typeof output === "string" ? [{ type: "text", text: output }] : output;
        try {
          await this._client._request(
            OP.submitToolCallResult,
            { agentID: call.agent_id, toolCallID: call.id },
            { ...scope, outcome, content_blocks },
            { ...options, signal: undefined },
          );
        } catch (error) {
          if (!(error instanceof ConflictError)) throw error;
        } finally {
          inFlight.delete(call.id);
        }
      })().catch(fail);
      running.add(task);
      void task.finally(() => running.delete(task));
    };

    const sweep = async () => {
      const pages = this._client._page<ListToolCallsResponse>(
        OP.listToolCalls,
        { agentID: agentId },
        { ...scope, state: "ready", type: "custom", include_subagents: true },
        { ...options, signal: controller.signal },
      );
      for await (const call of pages) handle(call);
    };

    const stream = this._client._stream<StreamEventsEvent>(
      OP.streamEvents,
      { agentID: agentId },
      { ...scope, ...(params.session_id ? { session_id: params.session_id } : {}) },
      { ...options, signal: controller.signal },
      { onOpen: () => void sweep().catch(fail), maxReconnects: params.max_reconnects ?? Number.POSITIVE_INFINITY },
    );

    const finished = (async () => {
      try {
        for await (const event of stream) {
          if (event.event !== "tool_call_update" || event.data.state !== "ready") continue;
          const { tool_call } = await this._client._request<ToolCallEnvelope>(
            OP.getToolCall,
            { agentID: event.data.agent_id ?? agentId, toolCallID: event.data.tool_call_id },
            scope,
            { ...options, signal: controller.signal },
          );
          handle(tool_call);
        }
      } catch (error) {
        if (!controller.signal.aborted) fail(error);
      }
      while (running.size > 0) await Promise.allSettled([...running]);
      if (failure !== undefined) throw failure;
    })();

    return {
      done: () => finished,
      stop: async () => {
        controller.abort();
        await finished;
      },
    };
  }
}
