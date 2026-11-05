// BMA extensions to the Anthropic Managed Agents API.
//
// The standard facade routes (/v1/agents, /v1/environments, /v1/sessions,
// events, events/stream, /v1/files, /v1/memory_stores) are served by the
// official Anthropic SDKs pointed at a BMA deployment. This module covers only
// the BMA extensions, as resources:
//
//   const ext = new FacadeExtensionsClient({ apiKey, baseUrl, projectId });
//   await ext.sessions.files.list(sessionId);
//
// Resource classes are generated from contracts/bma/facade-extensions.openapi.yaml
// and the `facade` section of contracts/bma/sdk.resources.yaml.
import { bmaOrigin } from "./core.js";
import { BmaError } from "./errors.js";
import { FacadeClientBase } from "./generated/facade-extensions-resources.js";

export type * from "./generated/facade-extensions-types.js";
export type * from "./generated/facade-extensions-operations.js";
export type { paths as FacadeExtensionPaths } from "./generated/facade-extensions.js";

export interface FacadeExtensionsOptions {
  /** BMA organization API key (sent as x-api-key). */
  apiKey: string;
  /** Deployment origin, without /v1 (for example https://api.bma.beeos.ai); the routes add /v1. */
  baseUrl: string;
  /** Default project (x-bma-project-id); required for multi-project keys. */
  projectId?: string;
  timeout?: number;
  maxRetries?: number;
  fetch?: typeof globalThis.fetch;
}

/**
 * Returns the BMA extension `bma_sequence` of a facade session event, or
 * undefined for preview and synthetic events. Send it as `Last-Event-ID` to
 * resume `GET /v1/sessions/{id}/events/stream`.
 */
export function bmaSequence(event: { bma_sequence?: unknown }): number | undefined {
  const value = event.bma_sequence;
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0 ? value : undefined;
}

/** Client for the BMA extension routes of the Anthropic-compatible facade. */
export class FacadeExtensionsClient extends FacadeClientBase {
  constructor(options: FacadeExtensionsOptions) {
    const apiKey = options.apiKey?.trim();
    if (!apiKey) throw new BmaError("bma facade: apiKey is required");
    const baseUrl = bmaOrigin(options.baseUrl ?? "");
    if (!baseUrl) throw new BmaError("bma facade: baseUrl is required");
    if (baseUrl.endsWith("/v1")) throw new BmaError("bma facade: baseUrl must be the origin without /v1");
    super({
      baseUrl,
      fetch: options.fetch,
      timeout: options.timeout,
      maxRetries: options.maxRetries,
      headers: { "x-api-key": apiKey },
      scope: { project_id: options.projectId },
      scopeOption: { project_id: "projectId" },
    });
  }
}
