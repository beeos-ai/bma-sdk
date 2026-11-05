// Error classes. Names and status mapping follow @anthropic-ai/sdk
// (core/error.d.ts): one subclass per HTTP status the API documents, plus
// connection, timeout and abort errors. `code` is the contract's stable
// error code (components.schemas.ErrorCode, an x-extensible-enum).
import type { components } from "./generated/rest.js";

/** Contract error codes; unknown future codes still type-check as strings. */
export type ErrorCode = components["schemas"]["ErrorCode"] | (string & {});
type AgentConfigErrorIssue = components["schemas"]["AgentConfigErrorIssue"];

/** Base class of every error thrown by the SDK. */
export class BmaError extends Error {
  constructor(message: string, options?: { cause?: unknown }) {
    super(message, options);
    this.name = new.target.name;
  }
}

/** An error response from the API, or a request that never got one. */
export class BmaApiError<TStatus extends number | undefined = number | undefined> extends BmaError {
  /** HTTP status; undefined for connection errors and stream error frames. */
  readonly status: TStatus;
  readonly headers: Headers | undefined;
  /** Stable error code from the response body. */
  readonly code: ErrorCode | undefined;
  /** Parsed response body, if any. */
  readonly error: unknown;
  /** Field-level problems for agent config validation errors. */
  readonly issues: AgentConfigErrorIssue[] | undefined;
  /** Current file digest for file_content_conflict / expected_digest_required. */
  readonly currentDigest: string | undefined;
  /** Facade extensions only: the Anthropic-style `error.type`. */
  readonly type: string | undefined;

  constructor(
    status: TStatus,
    body: unknown,
    message: string | undefined,
    headers: Headers | undefined,
    options?: { cause?: unknown },
  ) {
    const wire = (typeof body === "object" && body !== null ? body : {}) as Record<string, unknown>;
    // Native API: {error: string, code}. Facade: {type: "error", error: {type, message, code}}.
    const nested = typeof wire.error === "object" && wire.error !== null ? (wire.error as Record<string, unknown>) : undefined;
    const code = str(nested ? nested.code : wire.code);
    const type = nested ? str(nested.type) : undefined;
    const detail = str(nested ? nested.message : wire.error) ?? message;
    super(
      status === undefined
        ? (message ?? detail ?? "bma: request failed")
        : `bma: ${status} ${code ?? type ?? "unknown"}: ${detail ?? `HTTP ${status}`}`,
      options,
    );
    this.status = status;
    this.headers = headers;
    this.code = code;
    this.type = type;
    this.error = body;
    this.issues = Array.isArray(wire.issues) ? (wire.issues as AgentConfigErrorIssue[]) : undefined;
    this.currentDigest = str(wire.current_digest);
  }

  /** @internal */
  static generate(status: number, body: unknown, headers: Headers): BmaApiError {
    const cls = STATUS_CLASSES.get(status) ?? (status >= 500 ? InternalServerError : BmaApiError);
    return new cls(status, body, undefined, headers);
  }
}

function str(value: unknown): string | undefined {
  return typeof value === "string" && value !== "" ? value : undefined;
}

export class APIConnectionError extends BmaApiError<undefined> {
  constructor({ message, cause }: { message?: string; cause?: unknown } = {}) {
    super(undefined, undefined, message ?? "bma: connection error", undefined, { cause });
  }
}
export class APIConnectionTimeoutError extends APIConnectionError {
  constructor({ message }: { message?: string } = {}) {
    super({ message: message ?? "bma: request timed out" });
  }
}
export class APIUserAbortError extends BmaApiError<undefined> {
  constructor({ message }: { message?: string } = {}) {
    super(undefined, undefined, message ?? "bma: request was aborted", undefined);
  }
}

/**
 * An `error` frame on an event stream. The stream ends after it; frames with
 * code `service_unavailable` are retried by the SDK before this is thrown.
 */
export class EventStreamError extends BmaApiError<undefined> {
  constructor(body: unknown) {
    const wire = (body ?? {}) as { error?: unknown; code?: unknown };
    super(undefined, body, `bma: event stream error ${String(wire.code ?? "unknown")}: ${String(wire.error ?? "")}`, undefined);
  }
}

export class BadRequestError extends BmaApiError<400> {}
export class AuthenticationError extends BmaApiError<401> {}
export class PermissionDeniedError extends BmaApiError<403> {}
export class NotFoundError extends BmaApiError<404> {}
export class RequestTimeoutError extends BmaApiError<408> {}
export class ConflictError extends BmaApiError<409> {}
export class ContentTooLargeError extends BmaApiError<413> {}
export class UnprocessableEntityError extends BmaApiError<422> {}
export class RateLimitError extends BmaApiError<429> {}
export class InternalServerError extends BmaApiError<number> {}
export class ServiceUnavailableError extends InternalServerError {}

const STATUS_CLASSES = new Map<number, new (s: number, b: unknown, m: undefined, h: Headers) => BmaApiError>([
  [400, BadRequestError as never],
  [401, AuthenticationError as never],
  [403, PermissionDeniedError as never],
  [404, NotFoundError as never],
  [408, RequestTimeoutError as never],
  [409, ConflictError as never],
  [413, ContentTooLargeError as never],
  [422, UnprocessableEntityError as never],
  [429, RateLimitError as never],
  [503, ServiceUnavailableError],
]);
