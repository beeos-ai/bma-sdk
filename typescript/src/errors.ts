import { APIError } from '@anthropic-ai/sdk';

/**
 * BMA's reason for an API error (`error.bma_error_code` of the Anthropic error
 * envelope, e.g. "idempotency_key_reused"), or undefined when `error` is not an
 * API error or has no code. Branch on it rather than on the message.
 * (`error.code` is its deprecated spelling, read until BMA removes it on
 * 2026-12-01; the official `errorCode` property is `error.details.error_code`,
 * which BMA does not set.)
 */
export function errorCode(error: unknown): string | undefined {
  if (!(error instanceof APIError)) return undefined;
  const inner = (error.error as { error?: { bma_error_code?: unknown; code?: unknown } } | undefined)?.error;
  for (const code of [inner?.bma_error_code, inner?.code]) {
    if (typeof code === 'string' && code !== '') return code;
  }
  return undefined;
}
