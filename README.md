# BMA SDKs

Go clients for the BMA public API, published from `beeos-ai/bma-sdks`.

The Go module lives in [`go/`](go) and is versioned as
`github.com/beeos-ai/bma-sdks/go`.

## Packages

| Package | Import | Purpose |
| --- | --- | --- |
| REST | `github.com/beeos-ai/bma-sdks/go/rest` | Typed client for the BMA REST API used by Beework: agents, inputs, events, interactions, custom tool calls, and artifacts. |
| Executor | `github.com/beeos-ai/bma-sdks/go/executor` | `bma.executor.v1` transport: token bootstrap, WebSocket registration, heartbeat, reconnect, dispatch, and tool-result idempotency. |

## Install

```bash
go get github.com/beeos-ai/bma-sdks/go@v0.1.0
```

## REST quick start

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
	client, err := bmarest.NewClient(bmarest.Options{Token: os.Getenv("BMA_TOKEN")})
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	project := bmarest.ProjectScope{OrgID: "org_...", ProjectID: "proj_..."}

	launch, err := client.CreateAgent(ctx, project, bmarest.CreateAgentRequest{
		Profile: "aprf_...",
		Name:    ptr("Beework"),
		InitialInput: &bmarest.AgentLaunchInitialInput{
			ContentBlocks: []bmarest.ContentBlock{bmarest.TextBlock("Start the task.")},
		},
	}, bmarest.RequestOptions{IdempotencyKey: "launch-1"})
	if err != nil {
		log.Fatal(err)
	}

	agent := bmarest.AgentScope{OrgID: project.OrgID, ProjectID: project.ProjectID, AgentID: launch.Agent.ID}
	stream, err := client.StreamEvents(ctx, agent, bmarest.StreamEventsOptions{})
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
			log.Printf("event %s sequence %d", frame.AgentEvent.EventKind, frame.AgentEvent.Sequence)
		case frame.ToolCallUpdate != nil:
			log.Printf("tool call %s is %s", frame.ToolCallUpdate.ToolCallID, frame.ToolCallUpdate.State)
		case frame.ModelOutputDelta != nil:
			log.Printf("delta %s", frame.ModelOutputDelta.Event.Kind)
		case frame.Error != nil:
			log.Printf("stream error %s (retryable=%v)", frame.Error.Code, frame.Error.Retryable())
		}
	}
}

func ptr(value string) *string { return &value }
```

The REST package covers the agent execution surface:

- `CreateAgent`, `ListAgents`, `GetAgent`, `ArchiveAgent`, `CancelAgent`
- `CreateAgentInput`, `ListBacklogInputs`, `CancelBacklogInput`, `MoveBacklogInput`, `PromoteBacklogInputToSteering`, `DemoteBacklogInputToQueued`
- `ListEvents`, `ListTurns`, `ListTurnEvents`, `StreamEvents`
- `ListInteractions`, `ResolveInteraction`
- `ListToolCalls`, `SubmitToolCallResult`
- `GetArtifact`, `GetArtifactContent`

This is a deliberately scoped, hand-written typed client over the BMA REST
contract `rest.openapi.yaml` (contract version 1.0.0), not a full generator
output. Organization, project, machine, config, and other management endpoints
are not exposed in v0.1.0. Add them when a consumer needs them rather than
shipping a large generated surface now.

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

## Development

```bash
cd go
go test ./...
go vet ./...
```

The executor test decodes the shared contract conformance fixture from
[`go/executor/testdata/conformance.json`](go/executor/testdata/conformance.json).

## Release

The Go module is tagged `go/v<version>`; the first release is `go/v0.1.0`.
[`release-go.yaml`](.github/workflows/release-go.yaml) runs on `go/v*` tags,
rejects tags whose commit is not on `main`, and runs `go test ./...` from
`go/`.

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
