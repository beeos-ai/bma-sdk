# @beeos-ai/bma-sdk

> This README describes the 1.x native client (`/api/v1`). For the Anthropic-shaped `/v1` API use the
> official Anthropic SDK with `base_url` set to your BMA origin; see the
> [root README](../README.md#quick-start-the-anthropic-sdks). `bma-sdk` 2.0 replaces the native client.

[![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk)

TypeScript client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml) and the
resource map [`contracts/bma/sdk.resources.yaml`](../contracts/bma/sdk.resources.yaml),
plus the BMA extensions to the Anthropic Managed Agents API.

| | |
| --- | --- |
| Version | 1.0.0 (tag `v1.0.0`), see [CHANGELOG](../CHANGELOG.md); upgrading from 0.4: [MIGRATION](../MIGRATION.md) |
| Contract | BMA REST snapshot recorded in [`contracts/bma/lock.json`](../contracts/bma/lock.json) |
| Node.js | 20 or newer; ESM |

```ts
import { BmaClient } from "@beeos-ai/bma-sdk";

const bma = new BmaClient({
  token: process.env.BMA_TOKEN!,
  baseUrl: process.env.BMA_BASE_URL!, // origin, e.g. https://api.staging.bma.beeos.ai
  orgId: "org_...",                    // defaults: also read from BMA_ORG_ID / BMA_PROJECT_ID
  projectId: "prj_...",
});

const { session } = await bma.agents.sessions.create(agentId, { idempotency_key: "task-1" });
await bma.agents.inputs.create(
  agentId,
  { session_id: session.id, content_blocks: [{ type: "text", text: "Plan my week." }] },
  { idempotencyKey: "input-1" },
);

for await (const ev of bma.agents.events.stream(agentId, { session_id: session.id, stream_deltas: true })) {
  switch (ev.event) {
    case "model_output":       console.log(ev.sequence, ev.data.content_blocks); break;
    case "tool_call_update":   console.log(ev.data.tool_call_id, ev.data.state); break;
    case "model_output_delta": console.log(ev.data); break;
  }
}
```

Set `baseUrl` to the origin of your BMA deployment (for example
`https://api.staging.bma.beeos.ai`; the default `https://api.bma.beeos.ai` does
not resolve yet). The client adds `/api/v1`; a value already ending in
`/api/v1` is accepted. `token` and `baseUrl` default to
`BMA_TOKEN` and `BMA_BASE_URL`, `orgId` and `projectId` to `BMA_ORG_ID` and
`BMA_PROJECT_ID`.

## Methods

Every contract operation is a method on a resource: path IDs are positional
arguments, `params` is the operation's query, header and body fields in one
object (wire names, snake_case), and `options` is the per-request
`{ timeout, maxRetries, signal, idempotencyKey, headers }`. Params and results
are the contract types; every schema is exported by name (`AgentSession`,
`ToolCall`, ...).

- **Scope.** `orgId` / `projectId` fill the organization and project of every
  method; pass `org_id` / `project_id` in params to override one call.
- **Lists.** Every list whose response is `{ data, next_<param> }` returns a
  `PagePromise`: `await` gives the first page (`page.data`,
  `page.hasNextPage()`, `page.getNextPage()`), and
  `for await (const agent of bma.agents.list())` walks every item. Besides
  `cursor` lists this covers `agents.events.list` (forward by
  `after_sequence`, backward when you pass `before_sequence`),
  `agents.sessions.list` (`before_id`), `agentSessions.list` (`after_id`),
  `agents.turns.list`, `agents.turns.events.list` and `files.list` (`page`).
- **Event stream.** `agents.events.stream()` yields frames discriminated by
  `event`; durable frames carry `id` and `sequence`. Like EventSource, it
  reconnects with `Last-Event-ID` set to the last durable frame when the
  connection drops, when the server ends the response (a deployment), or on
  an `error` frame with code `service_unavailable`; a frame cut off at the end
  is discarded. It never ends on its own: it throws once `maxRetries`
  reconnects in a row received no data (a heartbeat counts as data), and any
  other error frame throws `EventStreamError`.
- **Files.** Uploads take the bytes as `body` (`Blob`, `ArrayBuffer`, typed
  array or string); downloads (`files.download`, `agents.artifacts.download`,
  ...) return the `Response`. `agents.artifacts.downloadVerified(artifact, { maxBytes })`
  verifies the size and sha256 digest.

## Errors, retries, timeouts

Errors are `BmaApiError` subclasses named after the status, as in the
Anthropic SDK: `BadRequestError` (400), `AuthenticationError` (401),
`PermissionDeniedError` (403), `NotFoundError` (404), `ConflictError` (409),
`ContentTooLargeError` (413), `UnprocessableEntityError` (422),
`RateLimitError` (429), `InternalServerError` (5xx), `ServiceUnavailableError`
(503), plus `APIConnectionError`, `APIConnectionTimeoutError` and
`APIUserAbortError`. `error.code` is the contract's `ErrorCode`.

Each call retries twice by default (`maxRetries`) with exponential backoff,
honouring `retry-after-ms` / `retry-after`. Reads and operations that accept
an `Idempotency-Key` retry 408, 429, 5xx and connection errors; the SDK sends
a generated key (`bma-sdk-retry-<uuid>`) unless you pass `idempotencyKey`, and
reuses it across the retries. Other writes retry only 429, 503 and requests
that never reached the server. 409 is never retried. The timeout is 60 s per
attempt (`timeout`), measured until the response headers arrive; `0`
disables it. Uploads (binary and multipart bodies) get only a per-call
`timeout`, so a large file is never cut off by the client default (Node's
fetch still bounds connecting and waiting for headers). The `signal` also
aborts reading the response body. Every error the SDK throws is a
`BmaError`.

## Custom tools

A custom tool call waits in `ready` until a consumer submits its result.
`defineTool` takes any [Standard Schema](https://standardschema.dev) (zod 4.2+,
valibot, arktype) and `agents.toolCalls.runner` runs the matching calls of an
agent and its subagents:

```ts
import { z } from "zod";
import { ToolError, defineTool } from "@beeos-ai/bma-sdk";

const weather = defineTool({
  name: "get_weather",
  description: "Current weather",
  inputSchema: z.object({ city: z.string() }),
  run: async ({ city }) => {
    if (!city) throw new ToolError("city is empty"); // submitted as a failed result
    return `Sunny in ${city}`;                       // string or result content blocks
  },
});
// weather.definition is the agent config entry for tools.get_weather.

const runner = bma.agents.toolCalls.runner(agentId, { session_id: session.id, tools: [weather] });
// ... later
await runner.stop();
```

The runner reconnects its event stream without limit by default (backoff up
to 8 s; `max_reconnects` bounds it), lists ready calls again after each
reconnect, treats a 409 on submit (another consumer answered first) as
handled, and `done()` rejects with the error that stopped it; it never ends
silently.

## BMA extensions to the Anthropic facade

Use the official Anthropic SDK for `/v1/agents`, `/v1/environments`,
`/v1/sessions` and events. The routes BMA adds live in a separate entry point:

```ts
import { FacadeExtensionsClient, bmaSequence } from "@beeos-ai/bma-sdk/facade-extensions";

const ext = new FacadeExtensionsClient({ baseUrl: "https://host", apiKey: key, projectId: "prj_..." });
const ticket = await ext.sessions.desktop.stream(sessionId, { desktop_session_id, origin: location.origin });
await ext.sessions.files.upload(sessionId, { file: new File([bytes], "report.pdf") });
const page = await ext.sessions.files.list(sessionId, { limit: 100 });
```

The executor protocol (executor, harness and agent ends) is the separate
package [`@beeos-ai/bma-executor-sdk`](https://github.com/beeos-ai/bma-executor-sdk/tree/main/typescript).
