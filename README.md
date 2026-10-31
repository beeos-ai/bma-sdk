# BMA SDKs

Go, TypeScript and Python clients for the BMA public API, published from
`beeos-ai/bma-sdks`. Every operation and model is generated from
[`contracts/bma/`](contracts/bma): the native REST contract
(`rest.openapi.yaml`) and the BMA extensions to the Anthropic Managed Agents
facade (`facade-extensions.openapi.yaml`). The executor protocol types come from the
executor contract snapshot in [`contracts/bma/executor/`](contracts/bma/executor),
the same contract the BMA server and bmad use.

## Packages

Two SDK families share this repository and the BMA contract: **bma-sdk**
(REST + façade extensions, for applications calling the BMA API) and
**bma-executor-sdk** (the executor protocol: executor, harness and agent
ends). They version and release independently.

| SDK | Package | Purpose |
| --- | --- | --- |
| Go | `github.com/beeos-ai/bma-sdks/go/rest` | Every operation in `rest.openapi.yaml`: agents, agent sessions (create/get/list/update/archive, session model override incl. `expires_with_session`), inputs and events with `session_id`, the SSE stream, artifacts, machines, desktop and terminal sessions and connection tickets, configuration. |
| Go | `github.com/beeos-ai/bma-sdks/go/facadeext` | BMA extensions to the Anthropic facade: `/v1/sessions/{id}/desktop/stream`, `/v1/sessions/{id}/files` upload/list, and the `bma_sequence`, `Idempotency-Key`, `mcp_servers[].bma_auth` and model-override field types. |
| Go | `github.com/beeos-ai/bma-sdks/executor` (separate module, tag `executor/v*`) | Both ends of the executor protocol (`bma.executor.v1.1`, types generated from BMA `contracts/bma`; the harness also accepts `v1`). Executor end (`Client`): token bootstrap (environment key or machine token), pluggable transport (WebSocket, Unix socket, executor-listens local socket, in-process pipe), registration, heartbeat, reconnect with resume and lease expiry, session lifecycle, tool dispatch/cancel, retried results, artifact upload, the raw MCP channel. Execution core (`Core`): bash, file tools, stdio MCP supervisor, cleanup, multi-harness isolation, and registrable capabilities (`NewProcessCapability` for `process.*` with PTY/file transfer/Git credential hooks, `NewSkillInstallCapability`, or your own `Capability`). bmad is built on this core. Harness end (`Harness`): accepts executors and drives sessions, tool calls and MCP channels. |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | Typed REST client (`.`) and facade extensions (`./facade-extensions`). |
| TypeScript | [`@beeos-ai/bma-executor-sdk`](executor/typescript) | Executor, harness and agent ends of `bma.executor.v1.1` with generated types; WebSocket, WebSocket over a Unix socket or named pipe (`unix://`, `npipe://`), and in-process transports. |
| Python | [`bma-sdk`](python) | `bma_sdk.rest` (generated), `bma_sdk.BmaClient`, `bma_sdk.facade_extensions`. |
| Python | [`bma-executor-sdk`](executor/python) (`bma_executor_sdk`) | `bma.executor.v1.1` executor, harness and agent ends on asyncio, with types generated from [`contracts/bma/executor`](contracts/bma/executor); WebSocket, WebSocket over a Unix domain socket, and in-process transports. |

The standard Anthropic facade routes (`/v1/agents`, `/v1/environments`,
`/v1/sessions`, events, events/stream, `/v1/memory_stores`) are intentionally
not wrapped: use the official Anthropic SDKs with `base_url` set to the BMA
facade, and these packages only for what BMA adds.

Neither the native API nor executor protocol v1 has an artifact upload
endpoint. Files a caller supplies are uploaded through the facade extension
`POST /v1/sessions/{id}/files`; artifacts the agent produces are downloaded
with `DownloadArtifact`/`downloadArtifact`/`download_artifact`, which verify
size and sha256.

## Install

```bash
go get github.com/beeos-ai/bma-sdks/go@v0.4.0          # bma-sdk: rest, facadeext
go get github.com/beeos-ai/bma-sdks/executor@v0.4.0    # bma-executor-sdk
npm install @beeos-ai/bma-sdk @beeos-ai/bma-executor-sdk
pip install bma-sdk bma-executor-sdk
```

Go modules resolve from the `go/v*` and `executor/v*` tags. The npm and PyPI
packages are published by the `ts/v*`, `python/v*`, `executor-ts/v*` and
`executor-python/v*` tags.

## REST quick start

`go/rest/generated.go` is generated from the contract; only authentication,
error decoding, server-sent events, and artifact streaming are handwritten.
Sessions are addressed with the generated `*AgentSession*` methods and the
`SessionId` field of `CreateAgentInputParams`, `StreamEventsParams`,
`ListEventsParams` and `ListTurnsParams`.

```go
package main

import (
	"context"
	"errors"
	"io"
	"log"
	"os"

	bmarest "github.com/beeos-ai/bma-sdks/go/rest"
)

func main() {
	client, err := bmarest.New(bmarest.Options{Token: os.Getenv("BMA_TOKEN")})
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	const org, project = "org_...", "proj_..."

	resp, err := client.CreateAgentWithResponse(ctx, org, project,
		&bmarest.CreateAgentParams{IdempotencyKey: ptr(bmarest.IdempotencyKey("launch-1"))},
		bmarest.CreateAgentJSONRequestBody{
			Profile: ptr(bmarest.AgentProfileID("aprf_...")),
			Name:    ptr(bmarest.AgentName("Beework")),
			InitialInput: &bmarest.AgentLaunchInitialInput{
				ContentBlocks: []bmarest.TextContentBlock{
					bmarest.NewTextContentBlock("Start the task."),
				},
			},
		},
	)
	if err != nil {
		log.Fatal(err)
	}
	if err := bmarest.CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		log.Fatal(err)
	}
	if resp.JSON201 == nil {
		log.Fatal("launch did not return an agent")
	}
	agentID := resp.JSON201.Agent.Id

	stream, err := client.OpenEventStream(ctx, org, project, agentID,
		&bmarest.StreamEventsParams{StreamDeltas: ptr(true)})
	if err != nil {
		log.Fatal(err)
	}
	defer stream.Close()

	for {
		frame, err := stream.Next()
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		switch {
		case frame.AgentEvent != nil:
			kind, _ := frame.AgentEvent.Discriminator()
			log.Printf("event %s sequence %d", kind, frame.Sequence)
		case frame.ToolCallUpdate != nil:
			log.Printf("tool call %s is %s", frame.ToolCallUpdate.ToolCallId, frame.ToolCallUpdate.State)
		case frame.ModelOutputDelta != nil:
			log.Printf("delta for model call %s", frame.ModelOutputDelta.ModelCallContextId)
		case frame.Error != nil:
			log.Printf("stream error %s (retryable=%v)", frame.Error.Code, frame.Error.Retryable())
		}
	}
}

func ptr[T any](value T) *T { return &value }
```

The generated surface covers the whole contract, including:

- agents, agent inputs, the queued/steering backlog, and session status
  (`idle`, `running`, `rescheduling`, `terminated`)
- events, turns, turn events, and the SSE stream
- interactions and custom tool calls
- artifacts and artifact content
- project files, the file resources mounted into sessions, and artifact
  promotion to files
- organizations, projects, actors, secrets, and secret versions
- model provider configs, configured models, and project model grants
- machines, machine pools, machine grants, and desktop/terminal sessions
- an agent's persistent machines (create, list, delete), machine resume, and
  machine backups/restore
- agent profiles, agent configs, skills, memory stores, integrations, and the
  remaining contract groups

Artifact downloads use `DownloadArtifact`, which verifies the size and sha256
digest recorded on the artifact:

```go
var artifact bmarest.Artifact // returned by GetArtifactWithResponse
err := client.DownloadArtifact(ctx, artifact, 32<<20, w)
```

`CheckResponse` turns generated error bodies into `*bmarest.APIError`:

```go
if err := bmarest.CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
	var apiErr *bmarest.APIError
	if errors.As(err, &apiErr) && apiErr.Retryable() {
		// retry according to the caller's policy
	}
}
```

### Files: upload, mount, outputs

A project file is uploaded once and mounted into sessions by reference, so the
bytes are stored once and never copied per session. The machine executor
mirrors the mounts below `/mnt/session/uploads` (read-only) and uploads what
the agent writes to `/mnt/session/outputs` back into the session's scope, so
`list files?scope_id=<session>` returns the session's outputs.

```go
content, err := os.ReadFile("report.pdf")
if err != nil {
	log.Fatal(err)
}
uploaded, err := client.UploadFileWithBodyWithResponse(ctx, org, project,
	&bmarest.UploadFileParams{Filename: "report.pdf"},
	"application/octet-stream", bytes.NewReader(content),
)
if err != nil {
	log.Fatal(err)
}
if err := bmarest.CheckResponse(uploaded.HTTPResponse, uploaded.Body); err != nil {
	log.Fatal(err)
}
file := uploaded.JSON201
if file == nil {
	file = uploaded.JSON200 // replay of the same upload with the same Idempotency-Key
}
if file == nil {
	log.Fatal("upload returned no file")
}

mounted, err := client.AddSessionResourceWithResponse(ctx, org, project, agentID, sessionID,
	bmarest.AddSessionResourceJSONRequestBody{
		Type:      bmarest.FileResourceParamsTypeFile,
		FileId:    file.Id,
		MountPath: ptr("/mnt/session/uploads/reports/report.pdf"),
	},
)
if err != nil {
	log.Fatal(err)
}
if err := bmarest.CheckResponse(mounted.HTTPResponse, mounted.Body); err != nil {
	log.Fatal(err)
}
log.Printf("mounted %s at %s", mounted.JSON200.FileId, mounted.JSON200.MountPath)

produced, err := client.ListFilesWithResponse(ctx, org, project,
	&bmarest.ListFilesParams{ScopeId: ptr(sessionID)})
if err != nil {
	log.Fatal(err)
}
if err := bmarest.CheckResponse(produced.HTTPResponse, produced.Body); err != nil {
	log.Fatal(err)
}
for _, output := range produced.JSON200.Data {
	log.Printf("output %s %s (%d bytes)", output.Id, output.Filename, output.SizeBytes)
}
```

TypeScript sends the raw bytes with `bodySerializer` so openapi-fetch does not
JSON-encode them:

```ts
const where = { orgID, projectID };
const file = unwrap(
  await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/files", {
    params: { path: where, query: { filename: "report.pdf" } },
    body: (await readFile("report.pdf")) as unknown as string, // typed string; any BodyInit is sent as is
    bodySerializer: (body) => body,
    headers: { "Content-Type": "application/octet-stream" },
  }),
);
const mounted = unwrap(
  await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/sessions/{sessionID}/resources", {
    params: { path: { ...where, agentID, sessionID } },
    body: { type: "file", file_id: file.id, mount_path: "/mnt/session/uploads/reports/report.pdf" },
  }),
);
const outputs = unwrap(
  await bma.rest.GET("/orgs/{orgID}/projects/{projectID}/files", {
    params: { path: where, query: { scope_id: sessionID } },
  }),
);
for (const output of outputs.data) console.log(output.id, output.filename, output.size_bytes);
```

In Python the REST `File` model is generated as `ProjectFile`, because
`bma_sdk.rest.types.File` is the upload payload:

```python
from pathlib import Path

from bma_sdk.rest.api.files import add_session_resource, list_files, upload_file
from bma_sdk.rest.models import FileResourceParams
from bma_sdk.rest.types import File as Upload

file = unwrap(upload_file.sync_detailed(
    org, project, client=bma.rest,
    body=Upload(payload=Path("report.pdf").read_bytes()), filename="report.pdf",
))
mounted = unwrap(add_session_resource.sync_detailed(
    org, project, agent_id, session_id, client=bma.rest,
    body=FileResourceParams(type_="file", file_id=file.id, mount_path="/mnt/session/uploads/reports/report.pdf"),
))
outputs = unwrap(list_files.sync_detailed(org, project, client=bma.rest, scope_id=session_id))
for output in outputs.data:
    print(output.id, output.filename, output.size_bytes)
```

The facade mounts
a file into an existing session through `facadeext.Client.AddSessionResource`,
`FacadeExtensionsClient.addSessionResource` or
`FacadeExtensionsClient.add_session_resource`; `/v1/files` itself is the
standard Anthropic Files API surface and is served by the official Anthropic
SDKs.

## Executor integration guide

The Executor Protocol is documented in the BMA repository
([中文](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/README.zh-CN.md) · [English](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/README.md)):
roles, deployment shapes, one executor per computer, and what is available or
coming.

| I want to | Start here |
| --- | --- |
| Write an executor (a "hand" the BMA cloud or a local brain drives) | [Executor quick start](#executor-quick-start) below, then the [protocol reference](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/protocol-reference.md) ([中文](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/protocol-reference.zh-CN.md)) and the [quick start](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/quickstart.md) ([中文](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/quickstart.zh-CN.md)) |
| Drive an executor (be the harness / local brain) | [local connection and auth](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/local-connection.md) ([中文](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/local-connection.zh-CN.md)); the Go `Harness` is coming in #4 |
| Connect a full local agent (turns in, agent events out) | [agent capability (draft)](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/agent-capability.md) ([中文](https://github.com/beeos-ai/beeos-managed-agents/blob/main/docs/integrations/executor/agent-capability.zh-CN.md)) |

## Executor quick start

```go
package main

import (
	"context"
	"log"
	"os"

	bmaexecutor "github.com/beeos-ai/bma-sdks/executor"
)

func main() {
	client, err := bmaexecutor.NewClient(bmaexecutor.Options{
		EnvironmentKey: os.Getenv("BMA_ENVIRONMENT_KEY"),
		EnvironmentID:  os.Getenv("BMA_ENVIRONMENT_ID"),
		Executor: bmaexecutor.ExecutorInfo{
			Name: "beework-executor", OS: "linux", Arch: "arm64", Version: "0.1.0",
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	client.OnToolCall(func(ctx context.Context, call bmaexecutor.ToolCallParams) (bmaexecutor.ToolResultParams, error) {
		return bmaexecutor.ToolResultParams{
			SessionID:  call.SessionID,
			ToolCallID: call.ToolCallID,
			Outcome:    bmaexecutor.ToolOutcomeSucceeded,
			Content:    []bmaexecutor.ContentBlock{{Type: bmaexecutor.ContentBlockTypeText, Text: "ok"}},
		}, nil
	})
	if _, err := client.Start(context.Background()); err != nil {
		log.Fatal(err)
	}
	select {}
}
```

Executor types follow one mapping in Go: required members are values,
optional members are values with `omitempty` (named structs and nullable
members are pointers), enums are untyped constants, and opaque payloads such as
`ToolCallParams.Input` stay `json.RawMessage` (`call.DecodeInput()` decodes the
built-in `ToolInput`).

See
[`executor/client.go`](executor/client.go) for the full transport
behavior and [`executor/client_test.go`](executor/client_test.go) for a
working in-process example.

### Executor lifecycle, cancellation, and results

- `tool.cancel` from the harness cancels the `context.Context` passed to the
  `OnToolCall` handler. The client responds `{"canceled":true}` and reports the
  result with `outcome: "canceled"`; handlers must stop their process group when
  the context is done.
- A repeated `tool.call` with the same `tool_call_id` is acknowledged but not
  executed twice.
- Call `SessionReady` after workspace and MCP setup, and `SessionEnded` after
  every child process and MCP server has stopped. The SDK does not infer these
  transitions because only the adapter knows when setup and cleanup finished.
- `tool.result` is retried with exponential backoff on `-32009`
  (`executor_busy`), `-32004` (`timeout`), or `data.retryable: true`. Results are
  idempotent by `tool_call_id`. When every attempt fails, `OnToolResultLost` is
  called with the original result so the adapter can persist and replay it; the
  client never drops a result silently.
- Large output must be reported as artifact references, not base64 in
  `tool.result`. `NewArtifactRef` and `NewArtifactContentBlock` build those
  blocks; `Client.UploadArtifact` uploads the bytes (v1.1 §6.5) first.
- `OpenMCPChannel` opens the MCP channel through `Options.Dial` (a
  `ChannelTarget`; `?channel=mcp&session_id=...&server_key=...` on WebSocket
  transports, so it follows the control channel over WebSocket, a Unix socket
  or in-process) and exchanges raw MCP JSON-RPC frames. `Core` supervises stdio MCP servers on top of it (below); an adapter
  without `Core` supervises its own.
- Session handler errors that are an `*RPCError` keep their code and data on
  the wire (for example retryable `executor_busy`).

### Execution core: one hand, any brain

`Core` is the executor's execution core, independent of who drives it.
`core.Attach(brain, client)` installs the session and tool handlers on a
`Client`; attach one `Client` per harness. bmad and the desktop app run one
executor process whose core serves the BMA cloud and a local harness at the
same time:

```go
core, _ := bmaexecutor.NewCore(bmaexecutor.CoreOptions{WorkRoot: dir, MaxSessions: 8, MaxSessionsPerBrain: 4})
cloud, _ := bmaexecutor.NewClient(bmaexecutor.Options{EnvironmentKey: key, EnvironmentID: env, Executor: info, Capabilities: core.Capabilities()})
local, _ := bmaexecutor.NewClient(bmaexecutor.Options{EnvironmentID: "local", Executor: info, Capabilities: core.Capabilities(),
	TokenSource: bmaexecutor.StaticToken("ws://127.0.0.1:7777", localToken)})
_ = core.Attach("cloud", cloud)
_ = core.Attach("local", local)
```

- Capabilities: `core.Register(cap)` before `Attach` adds methods behind
  capability bits; `core.Capabilities()` advertises them. A `SessionScoped`
  capability gets the brain's `*CoreSession` (workspace, per-session `Value`
  state) and `OnSessionEnd` runs before `session.ended`. bmad registers
  `NewProcessCapability(core, ProcessOptions{FileTransfer, GitCredentials})`,
  `NewSkillInstallCapability(installer)` and its own `terminal.*` capability.
- Transports: `Options.Dial` defaults to WebSocket on `ws://`, `wss://` or
  `unix:///path.sock` (the TypeScript and Python URL form); `UnixSocketDialer(path)`
  reaches a harness on a local socket, `ListenUnixSocket(path, token)` makes
  the executor the listening side (0700 dir, 0600 socket, bearer token) for a
  local brain that calls `Harness.DialExecutor` (the brain also dials its
  sessions' MCP channels, again after a server restart), and `InProcessDialer(h, p)`
  runs brain and hand in one process (`Harness.ServeConn`). `session.MCP(key)`
  works on all of them.
- Tools: `bash` (login shell in its own process group, env limited to
  PATH/HOME/USER/LANG/TMPDIR plus request env and `CoreOptions.Env`;
  `CoreOptions.DenyEnv` names executor-private variables (bmad: every `BMA_*`
  but `BMA_HOME`) that no bash tool, process or stdio MCP server inherits and
  no request may set; `ProcessOptions.Env` is set on processes only;
  `tool.cancel`, the deadline, `timeout_ms` and `session.stop` kill the whole
  group; a non-zero exit is a succeeded call reporting `exit_code`), `read`/`write`/`edit`/`glob`/`grep`
  confined to the session workspace `WorkRoot/<brain>/<session>` (override
  with `CoreOptions.Workspace`). Other tools return `capability_unavailable`.
- stdio MCP: every `session.assign.mcp_servers[]` entry with
  `connection_origin: environment` starts one process per
  (brain, session, `server_key`), verifies `command_sha256` when given, runs
  the command without a shell, and bridges stdin/stdout lines to that
  server's MCP channel. If either side ends both are restarted with backoff
  (each channel sees a fresh server; re-initialize); after 5 consecutive
  failures the core sends `session.status` `error` / `mcp_unavailable: <key>`.
  `session.ready` follows the first start attempt of every server.
- Isolation: sessions are keyed by (brain, `session_id`); two brains may use
  the same id. A `tool.call` reaches only sessions its own brain assigned
; MCP channels and
  workspaces are per brain and session. An unknown session or unsupported tool
  is answered before the ack (`-32007` / `-32012`). Bash is not a sandbox: every brain runs
  as the executor's OS user, so only attach brains you trust with this machine.
- Capacity: `MaxSessions` (default 16) across brains and
  `MaxSessionsPerBrain` (default `MaxSessions`) per brain, so a cloud harness
  cannot starve the local one. A full core answers `session.assign` with
  `executor_busy` (-32009, `retryable: true`). A replayed assign is
  idempotent. `session.stop` waits for the session's processes, then the core
  sends `session.ended`.

## Harness quick start

`Harness` is the harness ("brain") end: an `http.Handler` that accepts
executor control and MCP channels and the API that drives them. It speaks the
same protocol as the BMA service, so the executor cannot tell them apart.

```go
harness := bmaexecutor.NewHarness(bmaexecutor.HarnessOptions{
	Authenticate: func(r *http.Request) (bmaexecutor.Principal, error) { ... }, // nil only on loopback
})
go http.Serve(listener, harness)

executor, _ := harness.WaitExecutor(ctx)
session, _ := executor.AssignSession(ctx, bmaexecutor.SessionAssignParams{SessionID: "sess_1", MCPServers: servers})
_ = session.Ready(ctx)
result, _ := session.CallTool(ctx, bmaexecutor.ToolCallParams{Tool: bmaexecutor.ToolNameBash, Input: bmaexecutor.ToolInput{Command: &cmd}})
mcp, _ := session.MCP(ctx, "echo") // raw MCP JSON-RPC: Write/Read
_ = session.Stop(ctx, "done")
```

- `Authenticate` sees every upgrade (control and MCP). A returned
  `Principal.ExecutorID` pins the identity: `resume.executor_id` must match and
  only that executor may open MCP channels for its sessions. Without it the
  harness trusts `resume.executor_id` (loopback only).
- `CallTool` is idempotent by `tool_call_id` (generated when empty): a repeat
  joins the in-flight call or returns the recorded result without
  re-dispatching. Canceling its context stops waiting only; `CancelTool` sends
  `tool.cancel`.
- `tool.result` for a session not bound to that executor is `-32007`
  `session_not_active`; for a call this harness never dispatched it is `-32002`
  `not_found` (not retryable); duplicates are `accepted: true`.
- Resume: a disconnected executor keeps its sessions and pending calls for
  `LeaseTTL` (default 60s). A reconnect with `resume.executor_id` attaches to
  the same `Executor`; sessions missing from `resume.active_sessions` end. A
  newer connection replaces the old one with close code 4004. Lease expiry,
  `executor.close` or a dropped session fails pending calls with
  `ErrToolOutcomeUnknown`: the tool may or may not have run.
- MCP channels are isolated by (`session_id`, `server_key`); a newer channel
  for the same key replaces the old one and the session's end closes all.
- Conformance: Go harness ↔ Go executor (`executor/*_test.go`), and
  TypeScript ↔ Go in both directions plus the agent capability
  (`typescript/test/interop.test.ts` drives the peers in
  [`executor/internal/conformance`](executor/internal/conformance)), and in the BMA
  repository the SDK executor against the BMA server and the SDK harness
  against bmad's executor.
- Not in this release: a Python harness end; a TypeScript `Core`;
  `process.*`/`terminal.*` helpers of protocol v1.1; a durable result store
  (pending calls live in harness memory).

### Examples

- [`executor/examples/local-brain`](executor/examples/local-brain): a local harness with a
  scripted "model" drives `Core` over loopback: bash, then the stdio
  [`echo-mcp`](executor/examples/echo-mcp) server through the MCP channel.
  `cd go && go run ./examples/local-brain`
- [`executor/examples/cloud-hand`](executor/examples/cloud-hand): the same `Core` as a
  hand for the BMA cloud harness.
  `BMA_BASE_URL=... BMA_ENVIRONMENT_ID=... BMA_ENVIRONMENT_KEY=... go run ./examples/cloud-hand`

### Agent executors (a complete local agent)

An executor that runs its own model loop and tools (for example a desktop
app) serves the `agent` capability: the platform sends natural-language turns,
the executor streams Anthropic Managed Agents events back.

```go
client.ServeAgent(myAgent, bmaexecutor.AgentCapability{
	Models:          []bmaexecutor.AgentModel{{ID: "my-model", ThinkingLevels: []string{"low", "high"}}},
	PermissionModes: []string{"default", "accept_edits"},
})
```

`myAgent` implements `AgentHandler`: `OpenTurn` reports the effective
configuration, `RunTurn` does the work with `turn.Emit` (durable events),
`turn.Delta` (streaming previews), `turn.Inputs()` (`turn.input`) and
`turn.RequestInteraction` (approvals and questions answered on any client),
and `CloseSession` releases the local conversation. The SDK assigns event ids
and sequences, resends unacknowledged events after a reconnect, and frames
every turn with `session.status_running` and a final `session.status_idle`
whose `turn_outcome` is `completed`, `canceled` or `failed`.

The harness side is `HarnessOptions.Agent` (`AgentPlatform`) plus
`Executor.StartTurn`, `SendTurnInput`, `CancelTurn`, `CloseAgentSession` and
`RespondInteraction`. `go run ./examples/agentexecutor` (from `go/`) walks the
whole flow against a simulated platform, including a dropped connection.

### Python executor

`bma_executor_sdk` (package `bma-executor-sdk`) is the asyncio counterpart of the Go `executor` module, with the same
three ends: `ExecutorClient` (executor), `Harness` (harness) and the agent
capability (`ExecutorClient.serve_agent` / `Harness(agent=...)`). Protocol
types are TypedDicts generated into `bma_executor_sdk/generated.py` from the
contract snapshot in `contracts/bma/executor` (BMA `make contract-sdk`), so
messages are plain JSON dicts.

```python
import asyncio, os
from bma_executor_sdk import ExecutorClient

async def main() -> None:
    client = ExecutorClient(
        environment_key=os.environ["BMA_ENVIRONMENT_KEY"],
        environment_id=os.environ["BMA_ENVIRONMENT_ID"],
        executor={"name": "beework-executor", "os": "linux", "arch": "arm64", "version": "0.1.0"},
    )

    async def on_tool_call(call):
        return {"session_id": call["session_id"], "tool_call_id": call["tool_call_id"],
                "outcome": "succeeded", "is_error": False, "content": [{"type": "text", "text": "ok"}]}

    client.on_tool_call(on_tool_call)
    await client.start()
    await asyncio.Event().wait()

asyncio.run(main())
```

Transports are chosen by the channel URL: `ws://`/`wss://`, or
`unix:///path/to.sock` for WebSocket over a Unix domain socket
(`Harness.serve_unix`). `Harness.inprocess_dialer()` connects a client in the
same event loop without a socket. Windows named pipes are not implemented yet.
Behavior matches the Go SDK: `tool.cancel` cancels the handler's task and
reports `outcome: "canceled"`; duplicate `tool.call` ids run once;
`tool.result` retries `-32009`/`-32004`/`retryable` errors and hands a lost
result to `on_tool_result_lost`; reconnect resumes with
`resume.executor_id`/`active_sessions`; close codes 1008, 4002, 4003 and 4004
stop the client (4001 and 4005 reconnect, per the v1.1 contract).

| Go (`bmaexecutor`) | Python (`bma_executor_sdk`) |
| --- | --- |
| `NewClient(Options{...})` | `ExecutorClient(environment_id=..., executor=..., ...)` |
| `Options.TokenSource`, `StaticToken(url, token)` | `token_source=`, `static_token(url, token)` |
| `Client.Start` / `Stop` / `State` / `ExecutorID` / `ConnectionID` / `ActiveSessions` | `start()` / `stop(reason)` / `state` / `executor_id` / `connection_id` / `active_sessions` |
| `OnToolCall` / `OnSessionAssign` / `OnSessionStop` / `OnDrain` / `OnRequest` / `OnNotification` | `on_tool_call` / `on_session_assign` / `on_session_stop` / `on_drain` / `on_request` / `on_notification` |
| `Call` / `Notify` / `ReportToolResult` / `SessionReady` / `SessionEnded` / `OpenMCPChannel` | `call` / `notify` / `report_tool_result` / `session_ready` / `session_ended` / `open_mcp_channel` |
| `ServeAgent(handler, AgentCapability)` | `serve_agent(handler, capability)` |
| `AgentHandler.OpenTurn` / `RunTurn` / `CloseSession` | `open_turn` / `run_turn` / `close_session` (async; cancellation = task cancel) |
| `AgentTurn.Emit` / `EmitWithID` / `NewEventID` / `Delta` / `Flush` / `Inputs()` / `RequestInteraction` / `CancelInteraction` | `emit` / `emit_with_id` / `new_event_id` / `await delta` / `await flush` / `inputs` (asyncio.Queue) / `request_interaction` / `cancel_interaction` |
| `NewHarness(HarnessOptions{...})`, `http.Handler` | `Harness(...)`, `await serve(host, port)` / `serve_unix(path)` / `inprocess_dialer()` |
| `HarnessOptions.Authenticate(*http.Request) (Principal, error)` | `authenticate(ConnectRequest) -> Principal` (raise to refuse) |
| `Harness.Executors` / `WaitExecutor` | `executors()` / `wait_executor()` |
| `Executor.AssignSession` / `Drain` / `Capabilities` / `Protocol` | `assign_session` / `drain` / `capabilities` / `protocol` |
| `Executor.StartTurn` / `SendTurnInput` / `CancelTurn` / `CloseAgentSession` / `RespondInteraction` / `AgentCapability` | `start_turn` / `send_turn_input` / `cancel_turn` / `close_agent_session` / `respond_interaction` / `agent_capability()` |
| `Session.Ready` / `CallTool` / `CancelTool` / `Stop` / `MCP` / `Done` / `EndReason` | `ready()` / `call_tool` / `cancel_tool` / `stop` / `mcp` / `wait_ended()`, `ended` / `end_reason` |
| `AgentPlatform` | `AgentPlatform` (Protocol: `acked_sequence`, `agent_event`, `agent_delta`, `interaction_requested`, `interaction_canceled`) |
| `ErrNotConnected` / `ErrClientStopped` / `ErrSessionEnded` / `ErrToolOutcomeUnknown` / `ErrAssignRejected` / `*RPCError` | `NotConnectedError` / `ClientStoppedError` / `SessionEndedError` / `ToolOutcomeUnknownError` / `AssignRejectedError` / `RPCError` |

Examples in [`executor/python/examples`](executor/python/examples): `executor_minimal.py`
(BMA or a local harness), `harness_loopback.py` (brain and hand in one
process, in-process or `--unix`), `agent_minimal.py` (agent capability with an
in-memory platform). `python/tests/test_executor_interop.py` runs the Python
executor against the Go harness (WebSocket and Unix socket) and the Python
harness against the Go executor, from `go/internal/interop`.

## Development

The executor contract snapshot and the executor types (`executor/generated.go`,
`executor/typescript/src/generated/executor.ts`, `executor/python/src/bma_executor_sdk/generated.py`)
are generated in the BMA repository: `make contract-sdk SDK_DIR=<this checkout>`.
`tools/check_contract.py` verifies them against `contracts/bma/executor/lock.json`.

```bash
./tools/generate.sh                                  # regenerate Go, TypeScript and Python
uv run --no-project --with pyyaml --with jsonschema \
  python tools/check_contract.py [--source ../beeos-managed-agents]
(cd go && go vet ./... && go test ./...)
(cd typescript && npm ci && npm run build && npm test)
(cd python && uv run pytest -q)
(cd executor && go vet ./... && go test -race ./...)
(cd executor/python && uv sync && uv run pytest -q)   # interop tests need Go
(cd executor/typescript && npm ci && npm run build && npm test)   # Go + Python interop
```

`tools/generate.sh` needs Python 3 with PyYAML, Go 1.24+, Node 20+ and uv; it
pins oapi-codegen v2.7.0, openapi-typescript 7.13.0 and openapi-python-client
0.26.2. Never edit generated files by hand. The SDK tests of all three
languages replay the same recorded exchanges in
[`contracts/bma/fixtures/sdk-contract.json`](contracts/bma/fixtures/sdk-contract.json),
which `tools/check_contract.py` validates against the contracts. See
[`contracts/bma/README.md`](contracts/bma/README.md) for refreshing the
contract.

`go test ./rest -run TestStagingReadOnlySmoke` calls a live deployment
read-only when `BMA_BASE_URL`, `BMA_ORG_API_KEY`, `BMA_ORG_ID` and
`BMA_PROJECT_ID` are set; otherwise it is skipped.

## Release

bma-sdk tags: `go/v<version>`, `ts/v<version>`, `python/v<version>`, matching
`typescript/package.json` and `python/pyproject.toml`. bma-executor-sdk tags:
`executor/v<version>` (Go module `github.com/beeos-ai/bma-sdks/executor`),
`executor-ts/v<version>` and `executor-python/v<version>`, matching
`executor/typescript/package.json` and `executor/python/pyproject.toml`.

Every tag workflow first runs
[`contract.yaml`](.github/workflows/contract.yaml) as a reusable workflow
(regenerate every SDK with no diff, contract drift check, Go, TypeScript and
Python tests), then rejects a tag whose commit is not on `main` or whose
version does not match the package manifest, and only then publishes.

| Tag | Workflow | Publishes | Credentials |
| --- | --- | --- | --- |
| `go/v*` | [`release-go.yaml`](.github/workflows/release-go.yaml) | nothing; Go modules come from the tag | none |
| `ts/v*` | [`release-typescript.yaml`](.github/workflows/release-typescript.yaml) | `@beeos-ai/bma-sdk` to npm with provenance | repository secret `NPM_TOKEN` and the `releases` environment |
| `python/v*` | [`release-python.yaml`](.github/workflows/release-python.yaml) | `bma-sdk` to PyPI | a PyPI Trusted Publisher on `bma-sdk` bound to this repository and workflow, and the `releases` environment |
| `executor/v*` | [`release-executor-go.yaml`](.github/workflows/release-executor-go.yaml) | nothing; the Go module comes from the tag | none |
| `executor-ts/v*` | [`release-executor-typescript.yaml`](.github/workflows/release-executor-typescript.yaml) | `@beeos-ai/bma-executor-sdk` to npm with provenance | `NPM_TOKEN` and the `releases` environment |
| `executor-python/v*` | [`release-executor-python.yaml`](.github/workflows/release-executor-python.yaml) | `bma-executor-sdk` to PyPI | a PyPI Trusted Publisher on `bma-executor-sdk` (workflow `release-executor-python.yaml`) and the `releases` environment |

`NPM_TOKEN` must be a granular npm access token with read and write access to
the `@beeos-ai` scope (a classic Automation token works too); the first publish
of a new scoped package needs that token because npm trusted publishing can
only be configured on an existing package. The PyPI publisher is configured on
the project's *Publishing* settings (or as a pending publisher while the
project does not exist yet) with owner `beeos-ai`, repository `bma-sdks`,
workflow `release-python.yaml`, and environment `releases`; the upload then
uses OIDC and needs no PyPI API token.

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
