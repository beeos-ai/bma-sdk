// Compile-time assertions: these only need to type-check (tsc runs before
// node --test). A regression to a weak type fails the build.
import { test } from "node:test";
import { expectTypeOf } from "expect-type";
import { z } from "zod";

import {
  BmaApiError,
  BmaClient,
  defineTool,
  type AgentSession,
  type AgentStreamEvent,
  type ErrorCode,
  type ModelOutputDelta,
  type ModelOutputEvent,
  type Page,
  type PagePromise,
  type ToolCallUpdate,
} from "../src/index.js";
import { FacadeExtensionsClient, type SessionFile } from "../src/facade-extensions.js";

declare const bma: BmaClient;
declare const ext: FacadeExtensionsClient;
const typeOnly = false;

test("type assertions compile", () => {
  if (!typeOnly) return;

  // Positional path IDs and typed params / results.
  expectTypeOf(bma.agents.sessions.create).parameter(0).toEqualTypeOf<string>();
  expectTypeOf(bma.agents.sessions.retrieve("agt", "ses")).resolves.toHaveProperty("session").toEqualTypeOf<AgentSession>();
  // @ts-expect-error session id is required
  void bma.agents.sessions.retrieve("agt");
  // @ts-expect-error unknown params field
  void bma.agents.sessions.create("agt", { nope: true });
  // @ts-expect-error content_blocks is required for inputs
  void bma.agents.inputs.create("agt", { session_id: "ses" });
  // @ts-expect-error wrong enum value
  void bma.agents.inputs.create("agt", { content_blocks: [], delivery_mode: "later" });
  // Scope overrides are accepted everywhere.
  void bma.agents.list({ org_id: "org", project_id: "prj", limit: 1 });

  // Cursor lists: await -> Page, for await -> item.
  expectTypeOf(bma.agents.list()).toMatchTypeOf<PagePromise<{ data: unknown[] }>>();
  expectTypeOf<Awaited<ReturnType<BmaClient["agents"]["list"]>>>().toHaveProperty("hasNextPage");
  expectTypeOf<Awaited<ReturnType<BmaClient["agents"]["list"]>>>().toMatchTypeOf<Page<{ data: unknown[] }>>();

  // 204 -> void, binary -> Response.
  expectTypeOf(bma.agents.machines.delete("agt", "mch")).resolves.toEqualTypeOf<void>();
  expectTypeOf(bma.files.content("file")).resolves.toEqualTypeOf<Response>();

  // Event stream frames narrow on `event`.
  const narrow = (ev: AgentStreamEvent) => {
    switch (ev.event) {
      case "model_output":
        expectTypeOf(ev.data).toEqualTypeOf<ModelOutputEvent>();
        expectTypeOf(ev.sequence).toEqualTypeOf<number>();
        break;
      case "tool_call_update":
        expectTypeOf(ev.data).toEqualTypeOf<ToolCallUpdate>();
        // @ts-expect-error best-effort frames carry no sequence
        void ev.sequence;
        break;
      case "model_output_delta":
        expectTypeOf(ev.data).toEqualTypeOf<ModelOutputDelta>();
        break;
    }
  };
  void narrow;
  // @ts-expect-error "error" frames are thrown, never yielded
  const bad: AgentStreamEvent["event"] = "error";
  void bad;

  // Errors carry the contract code union.
  expectTypeOf<BmaApiError["code"]>().toEqualTypeOf<ErrorCode | undefined>();
  const code: ErrorCode = "state_transition_conflict";
  void code;

  // Facade extension resources.
  expectTypeOf(ext.sessions.files.upload("ses", { file: new File([], "a") })).resolves.toEqualTypeOf<SessionFile>();
  // @ts-expect-error file must be a Blob, not a string
  void ext.sessions.files.upload("ses", { file: "text" });

  // defineTool infers the run() input from the schema.
  const weather = defineTool({
    name: "get_weather",
    description: "Current weather",
    inputSchema: z.object({ city: z.string(), days: z.number().optional() }),
    run: (input) => {
      expectTypeOf(input).toEqualTypeOf<{ city: string; days?: number | undefined }>();
      return `Sunny in ${input.city}`;
    },
  });
  void bma.agents.toolCalls.runner("agt", { tools: [weather] }).done();
});
