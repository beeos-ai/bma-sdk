/** A random Idempotency-Key for one extension create. It is computed once per
 * call, so the official client's automatic retries resend the same key and the
 * server replays the first result. */
export function newIdempotencyKey(): string {
  return globalThis.crypto.randomUUID();
}
