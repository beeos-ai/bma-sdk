export { BmaClient, DEFAULT_BASE_URL, type BmaClientOptions } from './client.js';
export { BmaClient as default } from './client.js';
export { SDK_VERSION } from './version.js';
export { errorCode } from './errors.js';
export {
  agentExtensions,
  environmentExtensions,
  eventExtensions,
  sessionExtensions,
  type AgentExt,
  type AgentExtParams,
  type AgentModelOverride,
  type AgentModelOverrideInput,
  type AgentModelOverridePatch,
  type EnvironmentDesktop,
  type EnvironmentExt,
  type EnvironmentExtParams,
  type EnvironmentMachine,
  type EventExt,
  type Harness,
  type SessionCreateExt,
  type SessionExt,
  type SessionUpdateExt,
} from './extensions.js';
export * from './generated/extensions-resources.js';
export type { components } from './generated/extensions.js';
export { BmaBeta, BmaEvents, BmaSessions, type SentStream } from './beta.js';
// The official error classes, so one import serves error handling.
export {
  AnthropicError,
  APIError,
  APIConnectionError,
  APIConnectionTimeoutError,
  APIUserAbortError,
  AuthenticationError,
  BadRequestError,
  ConflictError,
  ContentTooLargeError,
  GatewayTimeoutError,
  InternalServerError,
  NotFoundError,
  OverloadedError,
  PermissionDeniedError,
  PreconditionFailedError,
  RateLimitError,
  RequestTimeoutError,
  ServiceUnavailableError,
  UnprocessableEntityError,
} from '@anthropic-ai/sdk';
