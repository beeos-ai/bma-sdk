// agents.artifacts.download: artifact content verified against the size and
// sha256 digest recorded on the artifact.
import type { RequestOptions } from "../core.js";
import { BmaError } from "../errors.js";
import type { Artifact } from "../generated/rest-types.js";
import { OP } from "../generated/rest-operations.js";
import { APIResource } from "../resource.js";

export interface DownloadArtifactOptions extends RequestOptions {
  /** Explicit product limit; artifacts larger than this are refused. */
  maxBytes: number;
}

export class ArtifactsBase extends APIResource {
  /**
   * Downloads artifact content and verifies its size and sha256 digest. The
   * whole body is buffered, bounded by maxBytes.
   */
  async download(artifact: Artifact, options: DownloadArtifactOptions): Promise<Uint8Array<ArrayBuffer>> {
    const { maxBytes, ...request } = options;
    const size = artifact.size_bytes;
    if (!(maxBytes > 0)) throw new BmaError("bma: maxBytes is required");
    if (size === undefined || size < 0 || size > maxBytes) {
      throw new BmaError("bma: artifact size is missing or exceeds maxBytes");
    }
    const digest = artifact.digest ?? "";
    if (!/^sha256:[0-9a-f]{64}$/.test(digest)) throw new BmaError("bma: artifact digest must be sha256:<hex>");
    const response = await this._client._request<Response>(
      OP.getArtifactContent,
      { agentID: artifact.agent_id, artifactID: artifact.id },
      { org_id: artifact.org_id, project_id: artifact.project_id },
      request,
    );
    const bytes = await readAtMost(response, size + 1);
    if (bytes.byteLength !== size) throw new BmaError(`bma: artifact size = ${bytes.byteLength}, want ${size}`);
    const hash = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
    const actual = Array.from(hash, (b) => b.toString(16).padStart(2, "0")).join("");
    if (`sha256:${actual}` !== digest) throw new BmaError("bma: artifact digest mismatch");
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
