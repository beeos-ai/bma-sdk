import type { ClientCore } from "./core.js";

export type { ClientCore };

/** Base class of every generated resource. */
export class APIResource {
  /** @internal */
  protected readonly _client: ClientCore;

  constructor(client: ClientCore) {
    this._client = client;
  }
}
