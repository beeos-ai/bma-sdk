import { APIError } from '@anthropic-ai/sdk';

/**
 * BMA's reason for an API error (`error.code` of the Anthropic error envelope,
 * e.g. "idempotency_key_reused"), or undefined when `error` is not an API
 * error or has no code. Branch on it rather than on the message. (The
 * official `errorCode` property is `error.details.error_code`, which BMA does
 * not set.)
 */
export function errorCode(error: unknown): string | undefined {
  if (!(error instanceof APIError)) return undefined;
  const code = (error.error as { error?: { code?: unknown } } | undefined)?.error?.code;
  return typeof code === 'string' ? code : undefined;
}
