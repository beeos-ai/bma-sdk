import { APIConnectionError, APIError } from '@anthropic-ai/sdk/core/error';
import { Stream } from '@anthropic-ai/sdk/core/streaming';
import type { BaseAnthropic } from '@anthropic-ai/sdk/client';

/** Stream resumption: a dropped stream reconnects with Last-Event-ID, up to
 * `maxReconnects` attempts in a row with exponential backoff from `backoffMs`
 * to `maxBackoffMs`. Exported for the tests; not part of the public API. */
export const streamResume = { maxReconnects: 5, backoffMs: 500, maxBackoffMs: 8000 };

interface Frame {
  id?: string;
  bma_sequence?: number;
}

function retryableStatus(status: number | undefined): boolean {
  return status === 408 || status === 409 || status === 429 || (status !== undefined && status >= 500);
}

function isAbort(error: unknown): boolean {
  return error instanceof Error && (error.name === 'AbortError' || error.name === 'APIUserAbortError');
}

function sleep(ms: number, signal: AbortSignal): Promise<void> {
  return new Promise((resolve) => {
    const timer = setTimeout(done, ms);
    signal.addEventListener('abort', done, { once: true });
    function done() {
      clearTimeout(timer);
      signal.removeEventListener('abort', done);
      resolve();
    }
  });
}

/**
 * resumable wraps the official, non-resuming event stream `first`. When the
 * connection drops or the server ends the stream, it calls `connect` with the
 * Last-Event-ID to send and carries on with the new stream, so no event is lost
 * or repeated. One durable BMA event (a `bma_sequence`) projects into several
 * frames that share its sequence and the server resumes after a whole
 * sequence: it resumes after the previous sequence and skips the frames it
 * already returned. It stops when the stream is aborted, after `maxReconnects`
 * failed attempts in a row, or on an API error other than 408, 409, 429 and
 * 5xx (which the official client retries first). `after` is the Last-Event-ID
 * `first` was opened with (none: the server's default position); a reconnect
 * before any durable frame arrives reuses it, so the anchor survives a drop.
 */
export function resumable<Item extends object>(
  first: Stream<Item>,
  connect: (lastEventID: string | undefined) => Promise<Stream<Item>>,
  client: BaseAnthropic,
  signal?: AbortSignal | null,
  after?: number,
): Stream<Item> {
  const master = new AbortController();
  let current: Stream<Item> | undefined = first;
  master.signal.addEventListener('abort', () => current?.controller.abort());
  signal?.addEventListener('abort', () => master.abort(), { once: true });
  let consumed = false;

  async function* iterate(): AsyncGenerator<Item, void, undefined> {
    if (consumed) {
      throw new Error('Cannot iterate over a consumed stream, use `.tee()` to split the stream.');
    }
    consumed = true;
    let sequence = 0; // bma_sequence of the last durable frame
    let resumeAfter = after; // Last-Event-ID a reconnect sends
    const seen = new Set<string>(); // frame ids returned at `sequence`
    let failures = 0;
    try {
      for (;;) {
        let cause: unknown = new Error('stream ended');
        try {
          for await (const frame of current!) {
            const { id = '', bma_sequence: seq = 0 } = frame as Frame;
            if (seq > 0) {
              if (seq < sequence) continue; // replayed after a reconnect
              if (seq === sequence) {
                if (seen.has(id)) continue;
              } else {
                sequence = seq;
                resumeAfter = seq - 1;
                seen.clear();
              }
              seen.add(id);
            } else if (id !== '') {
              // An announcement ahead of its durable copy (such as the
              // session.status_idle of requires_action): a replay of the
              // current sequence must not return it twice.
              if (seen.has(id)) continue;
              seen.add(id);
            }
            failures = 0;
            yield frame;
          }
        } catch (error) {
          if (master.signal.aborted || isAbort(error)) return;
          if (error instanceof APIError && !(error instanceof APIConnectionError)) throw error;
          cause = error;
        }
        current?.controller.abort();
        for (;;) {
          if (master.signal.aborted) return;
          if (failures >= streamResume.maxReconnects) {
            throw new Error(`bma-sdk: event stream not resumed after ${failures} attempts`, { cause });
          }
          const delay = Math.min(streamResume.backoffMs * 2 ** failures, streamResume.maxBackoffMs);
          failures++;
          await sleep(delay, master.signal);
          if (master.signal.aborted) return;
          try {
            // Resume after the previous sequence; none yet means the anchor
            // the stream was opened with, or the server's default position
            // (new events only) without one.
            current = await connect(resumeAfter === undefined ? undefined : String(resumeAfter));
            break;
          } catch (error) {
            if (master.signal.aborted || isAbort(error)) return;
            if (error instanceof APIError && !(error instanceof APIConnectionError) && !retryableStatus(error.status)) {
              throw error;
            }
            cause = error;
          }
        }
      }
    } finally {
      master.abort();
    }
  }

  return new Stream(iterate, master, client);
}
