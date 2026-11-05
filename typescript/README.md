# @beeos-ai/bma-sdk

[![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk)

TypeScript client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml) and the
resource map [`contracts/bma/sdk.resources.yaml`](../contracts/bma/sdk.resources.yaml),
plus the BMA extensions to the Anthropic Managed Agents API.

| | |
| --- | --- |
| Version | see [CHANGELOG](../CHANGELOG.md); upgrading from 0.4: [MIGRATION](../MIGRATION.md) |
| Contract | BMA REST snapshot recorded in [`contracts/bma/lock.json`](../contracts/bma/lock.json) |
| Node.js | 20 or newer; ESM |

```ts
import { BmaClient } from "@beeos-ai/bma-sdk";

const bma = new BmaClient({
  token: process.env.BMA_TOKEN!,
  baseUrl: process.env.BMA_BASE_URL!, // API root including /v1
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

Set `baseUrl` to your BMA deployment, the API root including `/v1` (for
example `https://bma.example.com/api/v1`). The SDK does not read
`BMA_BASE_URL` itself.

## Methods

Every contract operation is a method on a resource: path IDs are positional
arguments, `params` is the operation's query, header and body fields in one
object (wire names, snake_case), and `options` is the per-request
`{ timeout, maxRetries, signal, idempotencyKey, headers }`. Params and results
are the contract types; every schema is exported by name (`AgentSession`,
`ToolCall`, ...).

- **Scope.** `orgId` / `projectId` fill the organization and project of every
  method; pass `org_id` / `project_id` in params to override one call.
- **Lists.** Cursor-paginated lists return a `PagePromise`: `await` gives the
  first page (`page.data`, `page.hasNextPage()`, `page.getNextPage()`), and
  `for await (const agent of bma.agents.list())` walks every item.
- **Event stream.** `agents.events.stream()` yields frames discriminated by
  `event`; durable frames carry `id` and `sequence`. An `error` frame with code
  `service_unavailable`, or a dropped connection, reconnects with
  `Last-Event-ID` set to the last durable frame (at most `maxRetries` times in
  a row); any other error frame throws `EventStreamError`.
- **Files.** Uploads take the bytes as `body` (`Blob`, `ArrayBuffer`, typed
  array or string); downloads (`files.content`, `agents.artifacts.content`,
  ...) return the `Response`. `agents.artifacts.download(artifact, { maxBytes })`
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
attempt (`timeout`).

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
