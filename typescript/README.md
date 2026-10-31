# @beeos-ai/bma-sdk

TypeScript client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml), plus
the BMA extensions to the Anthropic Managed Agents API.

```ts
import { BmaClient, unwrap } from "@beeos-ai/bma-sdk";

const bma = new BmaClient({ baseUrl: "https://host/api/v1", token: process.env.BMA_TOKEN! });
const path = { orgID: "org_...", projectID: "proj_...", agentID: "agt_..." };

const { session } = unwrap(
  await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/sessions", {
    params: { path },
    body: { idempotency_key: "task-1", model_override: { model: "deepseek-flash", expires_with_session: true /* ... */ } },
  }),
);
await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/inputs", {
  params: { path, query: { session_id: session.id } },
  body: { content_blocks: [{ type: "text", text: "Start." }] },
});
for await (const frame of bma.streamEvents({ ...path, sessionId: session.id })) {
  console.log(frame.event, frame.sequence);
}
```

`bma.rest` is a fully typed [openapi-fetch](https://openapi-ts.dev/openapi-fetch/)
client for every contract operation. `streamEvents` parses the SSE stream and
`downloadArtifact` verifies the artifact size and sha256 digest.

## BMA extensions to the Anthropic facade

Use the official Anthropic SDK for `/v1/agents`, `/v1/environments`,
`/v1/sessions` and events. The routes BMA adds live in a separate entry point:

```ts
import { FacadeExtensionsClient, bmaSequence } from "@beeos-ai/bma-sdk/facade-extensions";

const ext = new FacadeExtensionsClient({ baseUrl: "https://host", apiKey: key, projectId: "proj_..." });
const ticket = await ext.getSessionDesktopStream(sessionId, { desktopSessionId, origin: location.origin });
await ext.uploadSessionFile(sessionId, new Blob([bytes]), "report.pdf");
const page = await ext.listSessionFiles(sessionId, { limit: 100 });
```

It also exports the extension field types `ModelConfigOverride`
(`agent.model.api_url/api_key/api_format`), `MCPServerBMAAuth`
(`mcp_servers[].bma_auth`), `IDEMPOTENCY_KEY_HEADER`, and `bmaSequence(event)`
for `bma_sequence` resume cursors.

## Executor protocol (`@beeos-ai/bma-sdk/executor`)

The executor protocol (`bma.executor.v1.1` and `v1`) for Node.js 20+, with
the same three parts and behavior as [`go/executor`](../go/executor). Protocol
types are generated from the contract
([`src/generated/executor.ts`](src/generated/executor.ts), snapshot and lock in
[`contracts/bma/executor`](../contracts/bma/executor)); the runtime is
handwritten.

### Executor quick start

```ts
import { ExecutorClient } from "@beeos-ai/bma-sdk/executor";

const client = new ExecutorClient({
  environmentKey: process.env.BMA_ENVIRONMENT_KEY,
  environmentId: process.env.BMA_ENVIRONMENT_ID!,
  executor: { name: "my-executor", os: process.platform, arch: process.arch, version: "0.1.0" },
  capabilities: { shell: { enabled: true } },
});
client.handleTool("bash", async (call, { signal, progress }) => {
  progress("running");
  return { outcome: "succeeded", is_error: false, content: [{ type: "text", text: "ok" }] };
});
await client.start();
```

### Executor lifecycle, cancellation, and results

- `tool.cancel` aborts the handler's `signal` (so do `deadline_ms` and
  `stop()`); the client answers `{"canceled":true}` and reports
  `outcome: "canceled"`. A repeated `tool.call` id is acknowledged, not run
  twice. `handleTool(name, …)` routes one tool, `onToolCall` the rest.
- Call `sessionReady` after workspace/MCP setup and `sessionEnded` after
  cleanup. `tool.result` is retried on `-32009`, `-32004` or
  `data.retryable: true`, idempotent by `tool_call_id`; when every attempt
  fails `onToolResultLost` receives the result to persist and replay.
- Reconnect: exponential backoff (500 ms base, ×2, 30 s cap, jitter) with a
  fresh token per dial and `resume` (`executor_id`, `last_connection_id`,
  `active_sessions`). Close codes 1008, 4002, 4003, 4004 and 4005 are terminal;
  4001 (token expired) reconnects with a new token.
- `openMcpChannel(sessionId, serverKey)` opens the raw MCP channel
  (`?channel=mcp&session_id=&server_key=`); `read()`/`write()` carry MCP
  JSON-RPC frames unchanged.
- A handler that throws `RpcError` keeps its code and data on the wire.
  `onRequest(method, …)` serves `process.*`, `terminal.*` and `skill.install`.

### Harness quick start

```ts
import { Harness } from "@beeos-ai/bma-sdk/executor";

const harness = new Harness({ authenticate: (request) => verify(request) }); // omit only on loopback
const { url } = await harness.listen(); // or harness.attach(httpServer)

const executor = await harness.waitExecutor();
const session = await executor.assignSession({ session_id: "sess_1" });
await session.ready();
const result = await session.callTool({ tool: "bash", input: { command: "ls" } });
const mcp = await session.mcp("echo"); // raw MCP JSON-RPC
await session.stop("done");
```

Semantics match the Go `Harness`: `callTool` is idempotent by `tool_call_id`;
an unknown call's `tool.result` is `-32002`, a foreign session `-32007`;
sessions and pending calls survive a reconnect within `leaseTtlMs`; a newer
connection replaces the old one with 4004; lease expiry or `executor.close`
fails pending calls with `ToolOutcomeUnknownError`.

### Transports

Messages are identical on every transport; who dials is independent of the
protocol role (the executor always sends `executor.register` first).

| Transport | Executor end | Harness end |
| --- | --- | --- |
| WebSocket (cloud, executor dials) | default, or `webSocketDialer(...)` | `listen()`, `attach(server)`, `handleUpgrade(...)` |
| Local socket, executor dials | `dialer: localDialer({ path, token })` | `listenLocal({ path, token }, (conn, hello) => harness.accept(conn, ...))` |
| Local socket, harness dials (bmad listens) | `listenLocal(...)` → `new ExecutorClient({ dialer: async () => conn, reconnect: false })` | `harness.dialLocal({ path, token })` |
| In-process | `dialer: harness.inProcessDialer()` | — |

Local sockets are Unix domain sockets (0700 directory, 0600 socket) or Windows
named pipes. Each start writes a fresh local token (`createLocalToken`, 0600);
environment keys are never used locally. Framing is newline-delimited JSON
with a one-line `{"bma_hello":…}` handshake and `{"bma_close":{"code",…}}`
for WebSocket-equivalent close codes (see [`src/executor/local.ts`](src/executor/local.ts)).
The MCP channel is not available when the harness dials the executor.

### Agent executors

```ts
client.serveAgent(
  {
    openTurn: async (p) => ({ accepted: true, turn_id: p.turn_id, executor_session_ref: "conv_1", resumed: false, effective: {} }),
    runTurn: async (turn, signal) => {
      const answer = await turn.requestInteraction({ kind: "permission", tool_use_id: "tu_1", tool_name: "bash" }, signal);
      turn.emit({ type: "agent.message", content: [{ type: "text", text: answer.outcome }] });
    },
    closeSession: async () => {},
  },
  { models: [{ id: "my-model" }] },
);
```

The SDK assigns event ids and sequences, delivers events in order with
ACKs, resends after a reconnect, and frames each turn with
`session.status_running` and `session.status_idle` (`completed`, `canceled`,
`failed`). The harness side is `HarnessOptions.agent` (`AgentPlatform`) plus
`executor.startTurn / sendTurnInput / cancelTurn / closeAgentSession /
respondInteraction`; a sequence gap answers `-32013` with
`data.expected_sequence`.

### Examples

[`examples/ts`](../examples/ts) (`npm install` there first):
`executor-minimal` (cloud executor with bash), `harness-loopback` (bmad-style
local socket: executor listens, harness dials), `agent-minimal` (agent
executor and in-memory platform in one process).

### Go ↔ TypeScript

| Go (`go/executor`) | TypeScript (`@beeos-ai/bma-sdk/executor`) |
| --- | --- |
| `NewClient(Options)` / `Start` / `Stop` | `new ExecutorClient(options)` / `start()` / `stop()` |
| `Options.TokenSource`, `StaticToken` | `tokenSource`, `staticToken` (or `dialer`) |
| `OnToolCall(ctx, call)` | `onToolCall(call, { signal, progress })`, `handleTool(name, …)` |
| `OnSessionAssign` / `OnSessionStop` / `OnDrain` / `OnRequest` / `OnNotification` | `onSessionAssign` / `onSessionStop` / `onDrain` / `onRequest` / `onNotification` |
| `SessionReady` / `SessionEnded` / `ReportToolResult` | `sessionReady` / `sessionEnded` / `reportToolResult` |
| `SendSessionStatus` / `SendToolProgress` / `SendExecutorCapabilitiesUpdate` | `sessionStatus` / `toolProgress` / `updateCapabilities` |
| `OpenMCPChannel` → `MCPChannel` | `openMcpChannel` → `FrameChannel` |
| `ServeAgent(AgentHandler, AgentCapability)` | `serveAgent(handler, capability)` |
| `AgentTurn.Emit/EmitWithID/Delta/Flush/Inputs/RequestInteraction/CancelInteraction` | `emit/emitWithId/delta/flush/inputs/requestInteraction/cancelInteraction` |
| `NewHarness(HarnessOptions)` (`http.Handler`) | `new Harness(options)` + `listen/attach/handleUpgrade/accept/dialLocal/inProcessDialer` |
| `Harness.WaitExecutor` / `Executors` | `waitExecutor` / `executors` |
| `Executor.AssignSession/Drain/StartTurn/SendTurnInput/CancelTurn/CloseAgentSession/RespondInteraction` | `HarnessExecutor.assignSession/drain/startTurn/sendTurnInput/cancelTurn/closeAgentSession/respondInteraction` |
| `Session.Ready/CallTool/CancelTool/Stop/MCP/Done/EndReason` | `HarnessSession.ready/callTool/cancelTool/stop/mcp/done/endReason` |
| `AgentPlatform` | `AgentPlatform` |
| `*RPCError`, `ErrNotConnected`, `ErrClientStopped`, `ErrSessionEnded`, `ErrToolOutcomeUnknown`, `ErrAssignRejected` | `RpcError`, `NotConnectedError`, `ClientStoppedError`, `SessionEndedError`, `ToolOutcomeUnknownError`, `AssignRejectedError` |
| `Core` (bash/files/stdio MCP) | not provided |
| — (WebSocket only) | `listenLocal` / `dialLocal` / `inProcessPair` |

### Tests

`npm test` runs, besides the REST tests: the conformance examples against
both TS ends ([`test/conformance.test.ts`](test/conformance.test.ts)), executor ↔
harness over every transport with reconnect and lease
([`test/executor.test.ts`](test/executor.test.ts)), the agent capability
([`test/agent.test.ts`](test/agent.test.ts)), and interop with the Go SDK
([`test/interop.test.ts`](test/interop.test.ts): TS executor ↔ Go harness, TS
agent ↔ Go platform, TS harness ↔ Go executor; needs Go).
