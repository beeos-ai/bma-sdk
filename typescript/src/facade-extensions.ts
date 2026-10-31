// BMA extensions to the Anthropic Managed Agents API.
//
// The standard facade routes (/v1/agents, /v1/environments, /v1/sessions,
// events, events/stream, /v1/files, /v1/memory_stores) are served by the
// official Anthropic SDKs pointed at a BMA deployment. Everything in this module is a
// BMA extension that is NOT part of the Anthropic contract. Types come from
// src/generated/facade-extensions.ts, generated from
// contracts/bma/facade-extensions.openapi.yaml.
import createClient, { type Client } from "openapi-fetch";
import type { components, paths } from "./generated/facade-extensions.js";

export type { paths as FacadeExtensionPaths };
export type DesktopStream = components["schemas"]["DesktopStream"];
export type SessionFile = components["schemas"]["SessionFile"];
export type SessionFilePage = components["schemas"]["SessionFilePage"];
/** BMA extension: a project file mounted into a session. */
export type FileResource = components["schemas"]["FileResource"];
export type FileResourcePage = components["schemas"]["FileResourcePage"];
export type DeletedSessionResource = components["schemas"]["DeletedSessionResource"];
/** BMA extension: one downloaded session file with its response metadata. */
export interface SessionFileContent {
  content: Uint8Array;
  contentType: string | null;
  filename: string | null;
  digest: string | null;
}
/** BMA extension: session `agent.model` object with a write-only credential override. */
export type ModelConfigOverride = components["schemas"]["ModelConfigOverride"];
/** BMA extension: `mcp_servers[].bma_auth`. */
export type MCPServerBMAAuth = components["schemas"]["MCPServerBMAAuth"];

function dispositionFilename(value: string | null): string | null {
  if (!value) return null;
  const match = /filename\*?=(?:UTF-8'')?"?([^";]+)"?/i.exec(value);
  return match?.[1] ? decodeURIComponent(match[1]) : null;
}

/** BMA extension header forwarded on session create and send-events. */
export const IDEMPOTENCY_KEY_HEADER = "Idempotency-Key";

/**
 * Returns the BMA extension `bma_sequence` of a facade session event, or
 * undefined for preview and synthetic events. Send it as `Last-Event-ID` to
 * resume `GET /v1/sessions/{id}/events/stream`.
 */
export function bmaSequence(event: unknown): number | undefined {
  const value = (event as { bma_sequence?: unknown } | null)?.bma_sequence;
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : undefined;
}

export interface FacadeExtensionsOptions {
  /** BMA organization API key (sent as x-api-key). */
  apiKey: string;
  /** Facade origin, without /v1 (for example https://api.bma.beeos.ai). */
  baseUrl: string;
  /** Project to operate in (x-bma-project-id); required for multi-project keys. */
  projectId?: string;
  fetch?: typeof globalThis.fetch;
}

/** An Anthropic-style error envelope returned by a facade extension route. */
export class FacadeApiError extends Error {
  readonly status: number;
  readonly type: string;
  readonly code?: string;

  constructor(status: number, body: unknown) {
    const error = ((body as { error?: unknown } | null)?.error ?? {}) as { type?: unknown; message?: unknown; code?: unknown };
    const type = typeof error.type === "string" ? error.type : "api_error";
    const message = typeof error.message === "string" && error.message !== "" ? error.message : `HTTP ${status}`;
    super(`bma facade: HTTP ${status} ${type}: ${message}`);
    this.name = "FacadeApiError";
    this.status = status;
    this.type = type;
    this.code = typeof error.code === "string" ? error.code : undefined;
  }
}

function check<T>(result: { data?: T; error?: unknown; response: Response }): T {
  if (result.response.ok) return result.data as T;
  throw new FacadeApiError(result.response.status, result.error);
}

/** Client for the BMA extension routes of the Anthropic-compatible facade. */
export class FacadeExtensionsClient {
  readonly raw: Client<paths>;

  constructor(options: FacadeExtensionsOptions) {
    const apiKey = options.apiKey?.trim();
    if (!apiKey) throw new Error("bma facade: apiKey is required");
    const baseUrl = options.baseUrl?.trim().replace(/\/+$/, "");
    if (!baseUrl) throw new Error("bma facade: baseUrl is required");
    if (baseUrl.endsWith("/v1")) throw new Error("bma facade: baseUrl must be the origin without /v1");
    const headers: Record<string, string> = { "x-api-key": apiKey };
    if (options.projectId) headers["x-bma-project-id"] = options.projectId;
    this.raw = createClient<paths>({ baseUrl, headers, fetch: options.fetch ?? globalThis.fetch });
  }

  /** BMA extension: GET /v1/sessions/{session_id}/desktop/stream. */
  async getSessionDesktopStream(
    sessionId: string,
    options: { desktopSessionId: string; ttlSeconds?: number; origin?: string },
  ): Promise<DesktopStream> {
    return check(
      await this.raw.GET("/v1/sessions/{session_id}/desktop/stream", {
        params: {
          path: { session_id: sessionId },
          query: {
            desktop_session_id: options.desktopSessionId,
            ttl_seconds: options.ttlSeconds,
            origin: options.origin,
          },
        },
      }),
    );
  }

  /** BMA extension: POST /v1/sessions/{session_id}/files (multipart, at most 8 MiB). */
  async uploadSessionFile(sessionId: string, file: Blob, filename: string): Promise<SessionFile> {
    const form = new FormData();
    form.append("file", file, filename);
    return check(
      await this.raw.POST("/v1/sessions/{session_id}/files", {
        params: { path: { session_id: sessionId } },
        // The generated body type is the schema object; the wire body is FormData.
        body: form as unknown as { file: string },
        bodySerializer: (body) => body as unknown as FormData,
      }),
    );
  }

  /** BMA extension: GET /v1/sessions/{session_id}/files. */
  async listSessionFiles(sessionId: string, options: { limit?: number; page?: string } = {}): Promise<SessionFilePage> {
    return check(
      await this.raw.GET("/v1/sessions/{session_id}/files", {
        params: { path: { session_id: sessionId }, query: { limit: options.limit, page: options.page } },
      }),
    );
  }

  /** BMA extension: GET /v1/sessions/{session_id}/files/{file_id}/content. */
  async downloadSessionFile(sessionId: string, fileId: string): Promise<SessionFileContent> {
    const result = await this.raw.GET("/v1/sessions/{session_id}/files/{file_id}/content", {
      params: { path: { session_id: sessionId, file_id: fileId } },
      parseAs: "arrayBuffer",
    });
    if (!result.response.ok) throw new FacadeApiError(result.response.status, result.error);
    return {
      content: new Uint8Array(result.data as unknown as ArrayBuffer),
      contentType: result.response.headers.get("content-type"),
      filename: dispositionFilename(result.response.headers.get("content-disposition")),
      digest: result.response.headers.get("x-bma-file-digest"),
    };
  }

  /** BMA extension: POST /v1/sessions/{session_id}/resources. */
  async addSessionResource(sessionId: string, fileId: string, mountPath?: string): Promise<FileResource> {
    return check(
      await this.raw.POST("/v1/sessions/{session_id}/resources", {
        params: { path: { session_id: sessionId } },
        body: {
          type: "file",
          file_id: fileId,
          ...(mountPath === undefined ? {} : { mount_path: mountPath }),
        },
      }),
    );
  }

  /** BMA extension: GET /v1/sessions/{session_id}/resources. */
  async listSessionResources(sessionId: string): Promise<FileResourcePage> {
    return check(
      await this.raw.GET("/v1/sessions/{session_id}/resources", {
        params: { path: { session_id: sessionId } },
      }),
    );
  }

  /** BMA extension: DELETE /v1/sessions/{session_id}/resources/{resource_id}. */
  async deleteSessionResource(sessionId: string, resourceId: string): Promise<DeletedSessionResource> {
    return check(
      await this.raw.DELETE("/v1/sessions/{session_id}/resources/{resource_id}", {
        params: { path: { session_id: sessionId, resource_id: resourceId } },
      }),
    );
  }
}
