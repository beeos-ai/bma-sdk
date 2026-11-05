// Server-sent event streams.

/** A typed event stream. Iterate it once with `for await`; `abort()` closes it. */
export class Stream<T> implements AsyncIterable<T> {
  readonly controller: AbortController;
  #iterate: (signal: AbortSignal) => AsyncGenerator<T>;
  #used = false;

  /** @internal */
  constructor(iterate: (signal: AbortSignal) => AsyncGenerator<T>, controller: AbortController) {
    this.#iterate = iterate;
    this.controller = controller;
  }

  [Symbol.asyncIterator](): AsyncGenerator<T> {
    if (this.#used) throw new Error("bma: a Stream can be iterated only once");
    this.#used = true;
    return this.#iterate(this.controller.signal);
  }

  /** Closes the connection; a pending iteration ends with APIUserAbortError. */
  abort(): void {
    this.controller.abort();
  }
}

/** @internal One raw SSE frame. */
export interface RawSSEFrame {
  event: string;
  id?: string;
  data: string;
}

/** @internal Minimal text/event-stream parser (WHATWG SSE field rules). */
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
        const name = colon < 0 ? line : line.slice(0, colon);
        let value = colon < 0 ? "" : line.slice(colon + 1);
        if (value.startsWith(" ")) value = value.slice(1);
        if (name === "event") event = value;
        else if (name === "id") id = value;
        else if (name === "data") data.push(value);
      }
      if (done) {
        if (buffer.startsWith("data:")) data.push(buffer.slice(5).replace(/^ /, ""));
        const frame = dispatch();
        if (frame) yield frame;
        return;
      }
    }
  } finally {
    await reader.cancel().catch(() => undefined);
    reader.releaseLock();
  }
}
