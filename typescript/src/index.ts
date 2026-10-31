// TypeScript client for the BMA REST API. Every path, operation and schema
// type comes from src/generated/rest.ts, which is generated from
// contracts/bma/rest.openapi.yaml; this file adds only what the contract does
// not describe: bearer authentication, error decoding, the server-sent event
// stream, and verified artifact downloads.
import createClient, { type Client } from "openapi-fetch";
import type { components, operations, paths } from "./generated/rest.js";

export type { components, operations, paths };
export type Schemas = components["schemas"];

/** Hosted BMA API root, including the /v1 prefix. */
export const DEFAULT_BASE_URL = "https://api.bma.beeos.ai/v1";
export const SDK_VERSION = "0.3.0";

export interface BmaClientOptions {
  /** BMA personal or organization bearer token. */
  token: string;
  /** API root, for example https://api.bma.beeos.ai/v1 or https://host/api/v1. */
  baseUrl?: string;
  /** Optional fetch implementation; defaults to globalThis.fetch. */
  fetch?: typeof globalThis.fetch;
}

/** A non-2xx response from the BMA API. */
export class BmaApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly currentDigest?: string;
  readonly issues?: Schemas["AgentConfigErrorIssue"][];

  constructor(status: number, body: unknown) {
    const wire = (typeof body === "object" && body !== null ? body : {}) as Partial<Schemas["Error"]>;
    const code = typeof wire.code === "string" ? wire.code : "";
    const message = typeof wire.error === "string" && wire.error !== "" ? wire.error : `HTTP ${status}`;
    super(`bma: HTTP ${status} ${code || "unknown"}: ${message}`);
    this.name = "BmaApiError";
    this.status = status;
    this.code = code;
    this.currentDigest = wire.current_digest;
    this.issues = wire.issues;
  }

  /** Whether a retry may succeed without changing the request. */
  get retryable(): boolean {
    return (
      this.status === 408 ||
      this.status === 429 ||
      this.status >= 500 ||
      this.code === "service_unavailable" ||
      this.code === "rate_limited"
    );
  }
}

/**
 * Returns `data` from an openapi-fetch result or throws BmaApiError.
 *
 * ```ts
 * const agent = unwrap(await bma.rest.GET("/orgs/{orgID}/projects/{projectID}/agents/{agentID}", { params }));
 * ```
 */
export function unwrap<T>(result: { data?: T; error?: unknown; response: Response }): T {
  if (result.response.ok) {
    return result.data as T;
  }
  throw new BmaApiError(result.response.status, result.error);
}

type StreamParams = operations["streamEvents"]["parameters"];

export interface StreamEventsOptions {
  orgID: string;
  projectID: string;
  agentID: string;
  /** Agent session (ses_...). Omit for the agent's default session. */
  sessionId?: string;
  afterSequence?: number;
  /** Resume after this durable sequence (sent as Last-Event-ID). */
  lastEventId?: number;
  streamDeltas?: boolean;
  signal?: AbortSignal;
}

/** One SSE data frame. `data` is the parsed JSON payload. */
export interface StreamFrame {
  event: string;
  id?: string;
  /** Durable event sequence; set only for frames that carry an SSE id. */
  sequence?: number;
  data: Schemas["AgentEventStreamData"];
}

export interface DownloadArtifactOptions {
  /** Explicit product limit; artifacts larger than this are refused. */
  maxBytes: number;
  signal?: AbortSignal;
}

/** Authenticated BMA REST client. */
export class BmaClient {
  /** Generated, fully typed openapi-fetch client for every contract operation. */
  readonly rest: Client<paths>;
  readonly baseUrl: string;
  private readonly token: string;
  private readonly fetchImpl: typeof globalThis.fetch;

  constructor(options: BmaClientOptions) {
    const token = options.token?.trim();
    if (!token) {
      throw new Error("bma: token is required");
    }
    const baseUrl = (options.baseUrl?.trim() || DEFAULT_BASE_URL).replace(/\/+$/, "");
    const scheme = new URL(baseUrl).protocol;
    if (scheme !== "http:" && scheme !== "https:") {
      throw new Error("bma: baseUrl must use http or https");
    }
    this.baseUrl = baseUrl;
    this.token = token;
    this.fetchImpl = options.fetch ?? globalThis.fetch;
    this.rest = createClient<paths>({ baseUrl, fetch: this.fetchImpl, headers: this.headers() });
  }

  private headers(extra: Record<string, string> = {}): Record<string, string> {
    return { Authorization: `Bearer ${this.token}`, ...extra };
  }

  private async send(path: string, accept: string, headers: Record<string, string>, signal?: AbortSignal): Promise<Response> {
    const response = await this.fetchImpl(this.baseUrl + path, {
      method: "GET",
      headers: this.headers({ Accept: accept, ...headers }),
      signal,
    });
    if (!response.ok) {
      const text = await response.text();
      let body: unknown;
      try {
        body = JSON.parse(text);
      } catch {
        body = undefined;
      }
      throw new BmaApiError(response.status, body);
    }
    return response;
  }

  /**
   * Streams `GET .../agents/{agentID}/events/stream`. Heartbeat comments are
   * skipped; the iterator ends when the server closes the stream.
   */
  async *streamEvents(options: StreamEventsOptions): AsyncGenerator<StreamFrame> {
    const query: NonNullable<StreamParams["query"]> = {};
    if (options.sessionId !== undefined) query.session_id = options.sessionId;
    if (options.afterSequence !== undefined) query.after_sequence = options.afterSequence;
    if (options.streamDeltas !== undefined) query.stream_deltas = options.streamDeltas;
    const search = new URLSearchParams(Object.entries(query).map(([k, v]) => [k, String(v)])).toString();
    const path =
      `/orgs/${encodeURIComponent(options.orgID)}/projects/${encodeURIComponent(options.projectID)}` +
      `/agents/${encodeURIComponent(options.agentID)}/events/stream` +
      (search ? `?${search}` : "");
    const headers: Record<string, string> = {};
    if (options.lastEventId !== undefined) headers["Last-Event-ID"] = String(options.lastEventId);

    const response = await this.send(path, "text/event-stream", headers, options.signal);
    const media = (response.headers.get("Content-Type") ?? "").split(";")[0]!.trim();
    if (media !== "text/event-stream" || !response.body) {
      await response.body?.cancel();
      throw new Error(`bma: event stream content type = ${JSON.stringify(media)}`);
    }
    for await (const raw of parseSSE(response.body)) {
      const frame: StreamFrame = { event: raw.event, data: JSON.parse(raw.data) };
      if (raw.id !== undefined) {
        const sequence = Number(raw.id);
        if (!Number.isSafeInteger(sequence)) {
          throw new Error(`bma: invalid event id ${JSON.stringify(raw.id)}`);
        }
        frame.id = raw.id;
        frame.sequence = sequence;
      }
      yield frame;
    }
  }

  /**
   * Downloads artifact content and verifies the size and sha256 digest
   * recorded on the artifact. The whole body is buffered, bounded by maxBytes.
   */
  async downloadArtifact(artifact: Schemas["Artifact"], options: DownloadArtifactOptions): Promise<Uint8Array<ArrayBuffer>> {
    const size = artifact.size_bytes;
    if (!(options.maxBytes > 0)) throw new Error("bma: maxBytes is required");
    if (size === undefined || size < 0 || size > options.maxBytes) {
      throw new Error("bma: artifact size is missing or exceeds maxBytes");
    }
    const digest = artifact.digest ?? "";
    if (!/^sha256:[0-9a-f]{64}$/.test(digest)) {
      throw new Error("bma: artifact digest must be sha256:<hex>");
    }
    const path =
      `/orgs/${encodeURIComponent(artifact.org_id)}/projects/${encodeURIComponent(artifact.project_id)}` +
      `/agents/${encodeURIComponent(artifact.agent_id)}/artifacts/${encodeURIComponent(artifact.id)}/content`;
    const response = await this.send(path, "application/octet-stream", {}, options.signal);
    const bytes = await readAtMost(response, size + 1);
    if (bytes.byteLength !== size) {
      throw new Error(`bma: artifact size = ${bytes.byteLength}, want ${size}`);
    }
    const hash = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
    const actual = Array.from(hash, (b) => b.toString(16).padStart(2, "0")).join("");
    if (`sha256:${actual}` !== digest) {
      throw new Error("bma: artifact digest mismatch");
    }
    return bytes;
  }
}

async function readAtMost(response: Response, limit: number): Promise<Uint8Array<ArrayBuffer>> {
  const reader = response.body?.getReader();
  if (!reader) return new Uint8Array();
  const chunks: Uint8Array[] = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    total += value.byteLength;
    if (total >= limit) {
      await reader.cancel();
      break;
    }
  }
  const out = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return out;
}

interface RawSSEFrame {
  event: string;
  id?: string;
  data: string;
}

/** Minimal text/event-stream parser (WHATWG SSE field rules). */
export async function* parseSSE(body: ReadableStream<Uint8Array>): AsyncGenerator<RawSSEFrame> {
  const decoder = new TextDecoder();
  let buffer = "";
  let event = "";
  let id: string | undefined;
  let data: string[] = [];
  const dispatch = (): RawSSEFrame | undefined => {
    const frame = data.length > 0 ? { event: event || "message", id, data: data.join("\n") } : undefined;
    event = "";
    id = undefined;
    data = [];
    return frame;
  };
  const reader = body.getReader();
  try {
    for (;;) {
      const { done, value } = await reader.read();
      buffer += done ? decoder.decode() : decoder.decode(value, { stream: true });
      let newline: number;
      while ((newline = buffer.search(/\r\n|\r|\n/)) >= 0) {
        const line = buffer.slice(0, newline);
        buffer = buffer.slice(newline + (buffer.startsWith("\r\n", newline) ? 2 : 1));
        if (line === "") {
          const frame = dispatch();
          if (frame) yield frame;
          continue;
        }
        if (line.startsWith(":")) continue;
        const colon = line.indexOf(":");
        const field = colon < 0 ? line : line.slice(0, colon);
        let value = colon < 0 ? "" : line.slice(colon + 1);
        if (value.startsWith(" ")) value = value.slice(1);
        if (field === "event") event = value;
        else if (field === "id") id = value;
        else if (field === "data") data.push(value);
      }
      if (done) {
        if (buffer !== "") {
          // A final line without a terminator still belongs to the frame.
          const colon = buffer.indexOf(":");
          if (colon > 0 && buffer.slice(0, colon) === "data") {
            data.push(buffer.slice(colon + 1).replace(/^ /, ""));
          }
        }
        const frame = dispatch();
        if (frame) yield frame;
        return;
      }
    }
  } finally {
    reader.releaseLock();
  }
}
