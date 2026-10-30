# BMA SDKs

Go clients for the BMA public API, published from `beeos-ai/bma-sdks`.

The Go module lives in [`go/`](go) and is versioned as
`github.com/beeos-ai/bma-sdks/go`.

## Packages

| Package | Import | Purpose |
| --- | --- | --- |
| REST | `github.com/beeos-ai/bma-sdks/go/rest` | Generated client for every operation in `contracts/bma/rest.openapi.yaml`: agents, inputs, events, interactions, tool calls, artifacts, organizations, projects, machines, and configuration. |
| Executor | `github.com/beeos-ai/bma-sdks/go/executor` | `bma.executor.v1` transport: token bootstrap, WebSocket registration, heartbeat, reconnect, session lifecycle, tool dispatch/cancel, retried tool results, artifact references, and the raw MCP channel. |

## Install

```bash
go get github.com/beeos-ai/bma-sdks/go@v0.2.1
```

## REST quick start

`go/rest/generated.go` is generated from the contract; only authentication,
error decoding, server-sent events, and artifact streaming are handwritten.

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
  frames. Process supervision (spawn, stderr limits, restart backoff) and
  automatic reconnection remain adapter responsibilities in this release.

## Development

```bash
cd go
go test ./...
go vet ./...
```

The REST package is generated from
[`contracts/bma/rest.openapi.yaml`](contracts/bma/rest.openapi.yaml). Regenerate
it with:

```bash
./tools/generate-rest.sh
git diff --exit-code go/rest/generated.go
```

The script requires Python 3 with PyYAML and Go 1.24+. It pins
`oapi-codegen` v2.7.0 and writes `go/rest/generated.go`. Do not edit that file
by hand. The executor test decodes the shared contract conformance fixture from
[`go/executor/testdata/conformance.json`](go/executor/testdata/conformance.json).

## Release

The Go module is tagged `go/v<version>`. [`release-go.yaml`](.github/workflows/release-go.yaml)
runs only for `go/v*` tags, rejects tags whose commit is not on `main`, and runs
`go test ./...` and `go vet ./...` from `go/`. There is no push-to-main or
pull-request CI.

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
