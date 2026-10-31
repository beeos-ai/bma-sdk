# BMA SDKs

Go, TypeScript and Python clients for the BMA public API, published from
`beeos-ai/bma-sdks`. Every operation and model is generated from
[`contracts/bma/`](contracts/bma): the native REST contract
(`rest.openapi.yaml`) and the BMA extensions to the Anthropic Managed Agents
facade (`facade-extensions.openapi.yaml`).

## Packages

| SDK | Package | Purpose |
| --- | --- | --- |
| Go | `github.com/beeos-ai/bma-sdks/go/rest` | Every operation in `rest.openapi.yaml`: agents, agent sessions (create/get/list/update/archive, session model override incl. `expires_with_session`), inputs and events with `session_id`, the SSE stream, artifacts, machines, desktop and terminal sessions and connection tickets, configuration. |
| Go | `github.com/beeos-ai/bma-sdks/go/facadeext` | BMA extensions to the Anthropic facade: `/v1/sessions/{id}/desktop/stream`, `/v1/sessions/{id}/files` upload/list, and the `bma_sequence`, `Idempotency-Key`, `mcp_servers[].bma_auth` and model-override field types. |
| Go | `github.com/beeos-ai/bma-sdks/go/executor` | Both ends of the executor protocol (`bma.executor.v1`; the harness also accepts `v1.1`). Executor end (`Client`): token bootstrap, WebSocket registration, heartbeat, reconnect, session lifecycle, tool dispatch/cancel, retried tool results, artifact references, the raw MCP channel. Execution core (`Core`): bash, file tools, stdio MCP supervisor, cleanup, multi-harness isolation. Harness end (`Harness`): accepts executors and drives sessions, tool calls and MCP channels. |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | Typed REST client (`.`), facade extensions (`./facade-extensions`), and the executor end (`./executor`: protocol types, `ExecutorClient` with registration, heartbeat, session assign/stop, deduplicated tool calls, `tool.cancel` via `AbortSignal`, retried results; Node >= 22 or pass `WebSocket`). |
| Python | [`bma-sdk`](python) | `bma_sdk.rest` (generated), `bma_sdk.BmaClient`, `bma_sdk.facade_extensions`. |

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
go get github.com/beeos-ai/bma-sdks/go@v0.3.0
```

The TypeScript and Python packages are tagged `ts/v0.3.0` and
`python/v0.3.0`. Release tags publish them as `@beeos-ai/bma-sdk` on npm and
`bma-sdk` on PyPI, and until those credentials are configured (see
[Release](#release)) install them from the tag, for example
`pip install "git+https://github.com/beeos-ai/bma-sdks@python/v0.3.0#subdirectory=python"`.

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

- agents, agent inputs, and the queued/steering backlog
- events, turns, turn events, and the SSE stream
- interactions and custom tool calls
- artifacts and artifact content
- organizations, projects, actors, secrets, and secret versions
- model provider configs, configured models, and project model grants
- machines, machine pools, machine grants, and desktop/terminal sessions
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

## Executor quick start

```go
package main

import (
	"context"
	"log"
	"os"

	bmaexecutor "github.com/beeos-ai/bma-sdks/go/executor"
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
			Content:    []bmaexecutor.ContentBlock{{Type: bmaexecutor.ContentBlockTypeText, Text: strPtr("ok")}},
		}, nil
	})
	if _, err := client.Start(context.Background()); err != nil {
		log.Fatal(err)
	}
	select {}
}

func strPtr(value string) *string { return &value }
```

See
[`go/executor/client.go`](go/executor/client.go) for the full transport
behavior and [`go/executor/client_test.go`](go/executor/client_test.go) for a
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
  blocks. The executor protocol v1 has no artifact upload endpoint, so upload
  bytes through your deployment's artifact store and report only the reference.
- `OpenMCPChannel` dials
  `?channel=mcp&session_id=...&server_key=...` and exchanges raw MCP JSON-RPC
  frames. `Core` supervises stdio MCP servers on top of it (below); an adapter
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

- Tools: `bash` (own process group; `tool.cancel`, the deadline, `timeout_ms`
  and `session.stop` kill the whole group), `read`/`write`/`edit`/`glob`/`grep`
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
  (otherwise a failed result `session_not_active`); MCP channels and
  workspaces are per brain and session. Bash is not a sandbox: every brain runs
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
- Conformance: Go harness ↔ Go executor (`go/executor/*_test.go`), Go
  harness ↔ TypeScript executor (`typescript/test/executor.test.ts` drives
  [`go/internal/conformance/harness`](go/internal/conformance/harness)), and in
  the BMA repository the SDK executor against the BMA server and the SDK
  harness against bmad's executor.
- Not in this release: TypeScript and Python harness ends; TypeScript
  executor reconnect/resume and a TypeScript `Core`; `process.*`/`terminal.*`
  helpers of protocol v1.1; a durable result store (pending calls live in
  harness memory). The TypeScript protocol types are hand-mirrored from the Go
  generated types until the contract generator emits them.

### Examples

- [`go/examples/local-brain`](go/examples/local-brain): a local harness with a
  scripted "model" drives `Core` over loopback: bash, then the stdio
  [`echo-mcp`](go/examples/echo-mcp) server through the MCP channel.
  `cd go && go run ./examples/local-brain`
- [`go/examples/cloud-hand`](go/examples/cloud-hand): the same `Core` as a
  hand for the BMA cloud harness.
  `BMA_BASE_URL=... BMA_ENVIRONMENT_ID=... BMA_ENVIRONMENT_KEY=... go run ./examples/cloud-hand`

## Development

```bash
./tools/generate.sh                                  # regenerate Go, TypeScript and Python
uv run --no-project --with pyyaml --with jsonschema \
  python tools/check_contract.py [--source ../beeos-managed-agents]
(cd go && go vet ./... && go test ./...)
(cd typescript && npm ci && npm run build && npm test)
(cd python && uv run pytest -q)
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

Tags: `go/v<version>`, `ts/v<version>`, `python/v<version>`, in lockstep with
`typescript/package.json` and `python/pyproject.toml`.

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
