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
| Go | `github.com/beeos-ai/bma-sdks/go/executor` | `bma.executor.v1` transport: token bootstrap, WebSocket registration, heartbeat, reconnect, session lifecycle, tool dispatch/cancel, retried tool results, artifact references, and the raw MCP channel. |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | Typed REST client (`.`) and facade extensions (`./facade-extensions`). |
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
  frames. Process supervision (spawn, stderr limits, restart backoff) and
  automatic reconnection remain adapter responsibilities in this release.

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
