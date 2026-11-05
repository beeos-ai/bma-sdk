// Request runtime shared by every generated resource method: scope defaults,
// request encoding, retries with idempotency keys, timeouts, error decoding,
// pagination and event streams. Defaults are ADR 0012 decision D3.
import {
  APIConnectionError,
  APIConnectionTimeoutError,
  APIUserAbortError,
  BmaApiError,
  BmaError,
  EventStreamError,
} from "./errors.js";
import { PagePromise, type CursorPageBody } from "./pagination.js";
import { Stream, parseSSE } from "./streaming.js";

/** Default per-attempt timeout (D3). Streams are bounded only until headers arrive. */
export const DEFAULT_TIMEOUT_MS = 60_000;
/** Default retries after the first attempt (D3; @anthropic-ai/sdk uses 2). */
export const DEFAULT_MAX_RETRIES = 2;

/** Generated description of one contract operation. */
export interface OperationDescriptor {
  readonly id: string;
  readonly method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  readonly path: string;
  /** Path template name -> params key (scope params) or positional name. */
  readonly pathParams?: Readonly<Record<string, string>>;
  /** Query name -> serialization style. */
  readonly query?: Readonly<Record<string, string>>;
  /** Header name -> params key. */
  readonly headers?: Readonly<Record<string, string>>;
  readonly body?: "json" | "binary" | "multipart";
  readonly bodyRequired?: boolean;
  readonly multipartJSON?: readonly string[];
  readonly response: "json" | "void" | "binary" | "sse";
  /** The operation accepts an Idempotency-Key header. */
  readonly idempotency?: boolean;
}

/** Per-request options; every resource method takes them last. */
export interface RequestOptions {
  /** Per-attempt timeout in milliseconds. */
  timeout?: number;
  maxRetries?: number;
  signal?: AbortSignal;
  /**
   * Idempotency-Key for operations that declare it. When omitted the SDK
   * generates one and reuses it across the retries of this call.
   */
  idempotencyKey?: string;
  headers?: Record<string, string>;
}

/** A raw request body: file contents or bytes. */
export type Uploadable = Blob | ArrayBuffer | ArrayBufferView | string;

/** @internal A body that may be omitted entirely. */
export type OptionalBody<B> = B | { [K in keyof B]?: never };

/** @internal A multipart body whose binary fields take a Blob or File. */
export type MultipartBody<B, Files extends PropertyKey> = B extends unknown
  ? { [K in keyof B]: K extends Files ? Blob : B[K] }
  : never;

/** @internal */
export interface ClientCoreOptions {
  baseUrl: string;
  fetch?: typeof globalThis.fetch;
  timeout?: number;
  maxRetries?: number;
  /** Authentication and other headers sent on every request. */
  headers: Record<string, string>;
  /** Scope defaults keyed by params name (org_id, project_id). */
  scope: Record<string, string | undefined>;
  /** Client option that sets each scope default, for error messages. */
  scopeOption: Record<string, string>;
}

// Connection failures where the request provably never reached the server
// (resolution, refusal, connect timeout). Undici reports them in `cause.code`.
const UNDELIVERED = new Set(["ECONNREFUSED", "ENOTFOUND", "EAI_AGAIN", "ENETUNREACH", "EHOSTUNREACH", "UND_ERR_CONNECT_TIMEOUT"]);

function undelivered(error: unknown): boolean {
  for (let e: unknown = error, depth = 0; e && depth < 5; e = (e as { cause?: unknown }).cause, depth++) {
    const code = (e as { code?: unknown }).code;
    if (typeof code === "string" && UNDELIVERED.has(code)) return true;
  }
  return false;
}

interface Built {
  url: string;
  headers: Headers;
  body: BodyInit | undefined;
}

/** Retry budget state of one call. */
interface Attempts {
  readonly max: number;
  used: number;
}

function sleep(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) return reject(new APIUserAbortError());
    const timer = setTimeout(() => {
      signal?.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      clearTimeout(timer);
      reject(new APIUserAbortError());
    };
    signal?.addEventListener("abort", onAbort, { once: true });
  });
}

// Exponential backoff with up to 25% jitter: 0.5s, 1s, 2s ... capped at 8s
// (@anthropic-ai/sdk client.js calculateDefaultRetryTimeoutMillis).
function backoff(retry: number): number {
  return Math.min(0.5 * 2 ** retry, 8) * (1 - Math.random() * 0.25) * 1000;
}

// retry-after-ms, then retry-after (seconds or HTTP date), honoured when
// between 0 and 60 seconds, as in @anthropic-ai/sdk.
function retryAfter(headers: Headers | undefined): number | undefined {
  const ms = Number.parseFloat(headers?.get("retry-after-ms") ?? "");
  if (Number.isFinite(ms) && ms >= 0 && ms < 60_000) return ms;
  const raw = headers?.get("retry-after");
  if (raw) {
    const seconds = Number.parseFloat(raw);
    const delay = Number.isFinite(seconds) ? seconds * 1000 : Date.parse(raw) - Date.now();
    if (Number.isFinite(delay) && delay >= 0 && delay < 60_000) return delay;
  }
  return undefined;
}

/** @internal The transport every resource calls. */
export class ClientCore {
  readonly baseUrl: string;
  readonly #fetch: typeof globalThis.fetch;
  readonly #timeout: number;
  readonly #maxRetries: number;
  readonly #headers: Record<string, string>;
  readonly #scope: Record<string, string | undefined>;
  readonly #scopeOption: Record<string, string>;

  constructor(options: ClientCoreOptions) {
    const baseUrl = options.baseUrl.trim().replace(/\/+$/, "");
    const scheme = new URL(baseUrl).protocol;
    if (scheme !== "http:" && scheme !== "https:") throw new BmaError("bma: baseUrl must use http or https");
    this.baseUrl = baseUrl;
    this.#fetch = options.fetch ?? globalThis.fetch;
    this.#timeout = options.timeout ?? DEFAULT_TIMEOUT_MS;
    this.#maxRetries = options.maxRetries ?? DEFAULT_MAX_RETRIES;
    this.#headers = options.headers;
    this.#scope = options.scope;
    this.#scopeOption = options.scopeOption;
  }

  /** @internal */
  _request<T>(op: OperationDescriptor, path: Record<string, string>, params: object, options?: RequestOptions): Promise<T> {
    return (async () => {
      const built = this.#build(op, path, params, options);
      const response = await this.#send(op, built, options);
      return this.#decode<T>(op, response);
    })();
  }

  /** @internal */
  _page<R extends CursorPageBody>(
    op: OperationDescriptor,
    path: Record<string, string>,
    params: object,
    options?: RequestOptions,
  ): PagePromise<R> {
    return new PagePromise<R>((cursor) =>
      this._request<R>(op, path, cursor === undefined ? params : { ...params, cursor }, options),
    );
  }

  /**
   * @internal Event stream with the reconnect rule of the contract: an
   * `error` frame with code `service_unavailable` (or a dropped connection)
   * reconnects with Last-Event-ID set to the last durable frame; any other
   * error frame ends the stream with EventStreamError.
   */
  _stream<T>(
    op: OperationDescriptor,
    path: Record<string, string>,
    params: object,
    options?: RequestOptions,
    onOpen?: () => void,
  ): Stream<T> {
    const controller = new AbortController();
    if (options?.signal) {
      if (options.signal.aborted) controller.abort();
      else options.signal.addEventListener("abort", () => controller.abort(), { once: true });
    }
    const resumeKey = Object.entries(op.headers ?? {}).find(([name]) => name.toLowerCase() === "last-event-id")?.[1];
    const maxRetries = options?.maxRetries ?? this.#maxRetries;
    const self = this;
    async function* iterate(signal: AbortSignal): AsyncGenerator<T> {
      let current: Record<string, unknown> = { ...(params as Record<string, unknown>) };
      let lastId: string | undefined;
      let failures = 0;
      for (;;) {
        const built = self.#build(op, path, current, options);
        built.headers.set("Accept", "text/event-stream");
        const response = await self.#send(op, built, { ...options, signal }, true);
        if (!response.body) throw new BmaError("bma: event stream response has no body");
        onOpen?.();
        let lastError: BmaApiError;
        try {
          for await (const raw of parseSSE(response.body)) {
            const data: unknown = JSON.parse(raw.data);
            if (raw.event === "error") {
              const error = new EventStreamError(data);
              if (error.code !== "service_unavailable") throw error;
              throw new ReconnectSignal(error);
            }
            failures = 0;
            if (raw.id !== undefined) {
              const sequence = Number(raw.id);
              if (!Number.isSafeInteger(sequence)) throw new BmaError(`bma: invalid event id ${JSON.stringify(raw.id)}`);
              lastId = raw.id;
              yield { event: raw.event, id: raw.id, sequence, data } as T;
            } else {
              yield { event: raw.event, data } as T;
            }
          }
          return;
        } catch (error) {
          if (signal.aborted) throw new APIUserAbortError();
          if (error instanceof ReconnectSignal) lastError = error.error;
          else if (error instanceof BmaError || error instanceof SyntaxError) throw error;
          else lastError = new APIConnectionError({ cause: error });
        }
        if (failures >= maxRetries) throw lastError;
        await sleep(backoff(failures), signal);
        failures++;
        if (lastId !== undefined && resumeKey) {
          current = { ...(params as Record<string, unknown>), [resumeKey]: Number(lastId) };
          // Last-Event-ID is the resume point; after_sequence would replay older events.
          delete current.after_sequence;
        }
      }
    }
    return new Stream<T>(iterate, controller);
  }

  #build(op: OperationDescriptor, path: Record<string, string>, params: object, options?: RequestOptions): Built {
    const rest: Record<string, unknown> = { ...(params as Record<string, unknown>) };
    const headers = new Headers(this.#headers);

    let url = op.path;
    for (const [name, key] of Object.entries(op.pathParams ?? {})) {
      let value: unknown = path[name];
      if (value === undefined) {
        value = rest[key] ?? this.#scope[key];
        delete rest[key];
        if (typeof value !== "string" || value === "") {
          const option = this.#scopeOption[key] ?? key;
          throw new BmaError(`bma: ${op.id} needs ${key}; set the client option ${option} or pass ${key} in params`);
        }
      }
      url = url.replace(`{${name}}`, encodeURIComponent(String(value)));
    }

    const search = new URLSearchParams();
    for (const [name, style] of Object.entries(op.query ?? {})) {
      const value = rest[name];
      delete rest[name];
      if (value === undefined || value === null) continue;
      if (style === "deepObject" && typeof value === "object" && !Array.isArray(value)) {
        for (const [k, v] of Object.entries(value)) search.append(`${name}[${k}]`, String(v));
      } else if (Array.isArray(value)) {
        for (const v of value) search.append(name, String(v));
      } else {
        search.append(name, String(value));
      }
    }

    for (const [name, key] of Object.entries(op.headers ?? {})) {
      const value = rest[key] ?? (key in this.#scope ? this.#scope[key] : undefined);
      delete rest[key];
      if (value !== undefined && value !== null) headers.set(name, String(value));
    }

    if (op.idempotency) {
      headers.set("Idempotency-Key", options?.idempotencyKey ?? `bma-sdk-retry-${crypto.randomUUID()}`);
    } else if (options?.idempotencyKey !== undefined) {
      throw new BmaError(`bma: ${op.id} does not accept an Idempotency-Key`);
    }

    let body: BodyInit | undefined;
    if (op.body === "json") {
      if (op.bodyRequired || Object.keys(rest).length > 0) {
        body = JSON.stringify(rest);
        headers.set("Content-Type", "application/json");
      }
    } else if (op.body === "binary") {
      const raw = rest.body as Uploadable | undefined;
      if (raw !== undefined) {
        body = raw as BodyInit;
        headers.set("Content-Type", "application/octet-stream");
      }
    } else if (op.body === "multipart") {
      const form = new FormData();
      for (const [key, value] of Object.entries(rest)) {
        if (value === undefined) continue;
        if (value instanceof Blob) form.append(key, value, value instanceof File ? value.name : key);
        else if (op.multipartJSON?.includes(key) || typeof value === "object") form.append(key, JSON.stringify(value));
        else form.append(key, String(value));
      }
      body = form;
    }

    for (const [k, v] of Object.entries(options?.headers ?? {})) headers.set(k, v);
    const query = search.toString();
    return { url: this.baseUrl + url + (query ? `?${query}` : ""), headers, body };
  }

  /**
   * Sends with retries. GET and operations with an Idempotency-Key retry
   * 408/429/5xx and connection errors; other writes retry only requests that
   * never reached the server, 429 and 503 (D3). 409 is never retried.
   */
  async #send(op: OperationDescriptor, built: Built, options?: RequestOptions, headersOnly = false): Promise<Response> {
    const attempts: Attempts = { max: options?.maxRetries ?? this.#maxRetries, used: 0 };
    const safe = op.method === "GET" || op.idempotency === true;
    const timeout = options?.timeout ?? this.#timeout;
    for (;;) {
      const controller = new AbortController();
      const user = options?.signal;
      if (user?.aborted) throw new APIUserAbortError();
      const onAbort = () => controller.abort();
      user?.addEventListener("abort", onAbort, { once: true });
      let timedOut = false;
      const timer = setTimeout(() => {
        timedOut = true;
        controller.abort();
      }, timeout);
      let response: Response;
      try {
        response = await this.#fetch(built.url, {
          method: op.method,
          headers: built.headers,
          body: built.body,
          signal: controller.signal,
        });
      } catch (error) {
        clearTimeout(timer);
        user?.removeEventListener("abort", onAbort);
        if (user?.aborted) throw new APIUserAbortError();
        const failure = timedOut ? new APIConnectionTimeoutError() : new APIConnectionError({ cause: error });
        if (attempts.used < attempts.max && (safe || (!timedOut && undelivered(error)))) {
          await sleep(backoff(attempts.used++), user);
          continue;
        }
        throw failure;
      }
      clearTimeout(timer);
      if (!headersOnly || !response.ok) user?.removeEventListener("abort", onAbort);
      if (response.ok) return response;

      const text = await response.text().catch(() => "");
      let body: unknown;
      try {
        body = text ? JSON.parse(text) : undefined;
      } catch {
        body = undefined;
      }
      const error = BmaApiError.generate(response.status, body, response.headers);
      if (attempts.used < attempts.max && this.#shouldRetry(response, safe)) {
        await sleep(retryAfter(response.headers) ?? backoff(attempts.used), user);
        attempts.used++;
        continue;
      }
      throw error;
    }
  }

  #shouldRetry(response: Response, safe: boolean): boolean {
    const hint = response.headers.get("x-should-retry");
    if (hint === "false") return false;
    const s = response.status;
    if (!safe) return s === 429 || s === 503;
    if (hint === "true") return true;
    return s === 408 || s === 429 || s >= 500;
  }

  async #decode<T>(op: OperationDescriptor, response: Response): Promise<T> {
    if (op.response === "binary") return response as T;
    if (response.status === 204 || op.response === "void") {
      await response.body?.cancel();
      return undefined as T;
    }
    return (await response.json()) as T;
  }
}

class ReconnectSignal {
  constructor(readonly error: BmaApiError) {}
}
