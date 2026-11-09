# bma-sdk Go 2.0

`github.com/beeos-ai/bma-sdk/v2` (package `bmasdk`) is the complete BMA client
for servers (ADR 0025):

- The resources BMA shares with Claude Managed Agents — agents, environments,
  sessions, session events and resources, files, skills, vaults, memory
  stores — **are the official [anthropic-sdk-go](https://github.com/anthropics/anthropic-sdk-go)
  services** (pinned at v2.7.0): `client.Beta.Sessions.New` takes and returns
  `anthropic.BetaSessionNewParams` / `*anthropic.BetaManagedAgentsSession`.
  Code moves between the two SDKs unchanged.
- The BMA extensions — machines, machine pools and grants, desktop and
  terminal sessions with their tickets, organization projects — are generated
  from the BMA extension contract (`contracts/bma/v2/extensions.openapi.yaml`)
  and sit next to them under `client.Beta`.
- BMA extension fields on the shared objects (`bma_*`) are typed:
  `bmasdk.SessionExtensions(session)`, `EnvironmentExtensions`,
  `AgentExtensions`, `EventExtensions` read them, and
  `bmasdk.WithSessionModelOverride`, `WithHarness`, `WithEnvironmentDesktop`
  write them on the official methods.

Requires Go 1.25 or later (the official SDK's minimum). The 1.x native client
(`github.com/beeos-ai/bma-sdk`, repository root) is frozen.

> Server-side only. The API key is a tenant credential; end-user clients
> (browser, desktop app, phone) never get it. Give them a single-use ticket
> (`DesktopSessions.Tickets.New`, `TerminalSessions.Tickets.New`) instead.

## Install

```bash
go get github.com/beeos-ai/bma-sdk/v2
```

Until the `v2.0.0` tag is published, pin a commit of `main`
(`go get github.com/beeos-ai/bma-sdk/v2@<commit>`).

## Quick start

```go
import (
	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
	bmasdk "github.com/beeos-ai/bma-sdk/v2"
)

client := bmasdk.NewClient(
	option.WithAPIKey(apiKey),                                // default BMA_API_KEY
	option.WithBaseURL("https://api.staging.bma.beeos.ai"),   // origin; default BMA_BASE_URL, else https://api.bma.beeos.ai
	bmasdk.WithProject(projectID),                            // x-bma-project-id; default BMA_PROJECT_ID
)

session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agentID)},
	EnvironmentID: environmentID,
}, bmasdk.WithIdempotencyKey(requestID))

// Open the stream, then send. A dropped stream resumes by itself.
stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
defer stream.Close()
_, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
		Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{OfText: &anthropic.BetaManagedAgentsTextBlockParam{Text: "hello"}}},
	}}},
})
for stream.Next() {
	ev := stream.Current()
	ext, _ := bmasdk.EventExtensions(ev) // ext.Sequence, ext.ErrorCode, ...
	switch ev.Type {
	case "agent.custom_tool_use":
		// run the tool, then Send a user.custom_tool_result with CustomToolUseID: ev.ID
	case "session.status_idle":
		if ev.StopReason.Type != "requires_action" {
			return
		}
	}
}

// Or send first: SendAndStream opens the stream at the cursor read before the
// send (bma_resume_cursor), so frames an executor wrote before the stream
// opened are not lost. res.Replayed is true when the server gave no cursor and
// the stream starts at Last-Event-ID 0 (pick your turn by ext.InputID).
res, err := client.Beta.Sessions.Events.SendAndStream(ctx, session.ID, sendParams, anthropic.BetaSessionEventStreamParams{})
if err == nil {
	defer res.Stream.Close()
	// res.Sent is the send response; res.Stream yields this message's user.message first
}

// Extensions
machines := client.Beta.Machines.ListAutoPaging(ctx, bmasdk.MachineListParams{Limit: bmasdk.Ptr[int64](50)})
for machines.Next() {
	m := machines.Current()
	_ = m
}
term, err := client.Beta.TerminalSessions.New(ctx, bmasdk.TerminalSessionNewParams{MachineID: machineID})
ticket, err := client.Beta.TerminalSessions.Tickets.New(ctx, term.ID, bmasdk.TerminalSessionTicketNewParams{})
// hand ticket.Ticket, ticket.WsURL and ticket.Subprotocol to the end-user client; never log the ticket
```

## Behavior

| Topic | bma-sdk 2.0 | Official SDK |
|---|---|---|
| Credentials | `BMA_API_KEY`, `BMA_BASE_URL`, `BMA_PROJECT_ID`; never reads `ANTHROPIC_*`; base URL always BMA | `ANTHROPIC_API_KEY` …, default `https://api.anthropic.com` |
| Auth header | official: `option.WithAPIKey` → `Authorization: Bearer` (2.x); BMA accepts it and `x-api-key` | same |
| Errors | `*anthropic.Error` (`bmasdk.Error`): `StatusCode`, `RequestID`, `Type()`, `Message`; BMA's reason with `bmasdk.ErrorCode(err)` (`error.code`) | `*anthropic.Error` |
| Retries | official: 2 retries on 408/409/429/5xx and connection errors, `x-should-retry`, `retry-after(-ms)`; `option.WithMaxRetries` | same |
| Idempotency | extension creates and actions that accept it send a random `Idempotency-Key` (the same on every retry); `bmasdk.WithIdempotencyKey` sets it for any call, including the official methods | no idempotency header |
| Pagination | official `PageCursor` for shared resources; extensions return `*bmasdk.Page[T]` (`Data`, `NextPage`, `GetNextPage`) and `*bmasdk.PageAutoPager[T]` (`Next`, `Current`, `Err`, `Index`, `All`) | `PageCursor` / `PageCursorAutoPager` |
| Event stream | `Sessions.Events.StreamEvents` resumes a dropped stream with `Last-Event-ID` (the `bma_sequence` before the last frame's; frames already returned are skipped), up to 5 attempts in a row with backoff 0.5–8 s; API errors other than 408/409/429/5xx end it. `Sessions.Events.BetaSessionEventService.StreamEvents` is the official one | no reconnect |

Known server gap (staging, 2026-11-08): a stream resumed with `Last-Event-ID`
replays the durable events but not the `session.status_*` events the list
derives for them (ids `sesst_…`, e.g. the `session.status_idle` of
`requires_action`). Do not rely on that idle after a reconnect: the
`agent.custom_tool_use` event is enough to answer.

## Method signatures against anthropic-sdk-go

Shared resources: identical — `client.Beta.<Resource>` is the official service
value, so every method below has the official signature byte for byte.

| Resource | Methods (official v2.7.0) | In bma-sdk 2.0 |
|---|---|---|
| `Beta.Agents` | `New(ctx, BetaAgentNewParams, ...option.RequestOption) (*BetaManagedAgentsAgent, error)`, `Get(ctx, agentID, BetaAgentGetParams, ...)`, `Update(ctx, agentID, BetaAgentUpdateParams, ...)`, `List(ctx, BetaAgentListParams, ...) (*pagination.PageCursor[BetaManagedAgentsAgent], error)`, `ListAutoPaging`, `Archive(ctx, agentID, BetaAgentArchiveParams, ...)`; `Versions` | same |
| `Beta.Environments` | `New`, `Get`, `Update`, `List`, `ListAutoPaging`, `Delete`, `Archive` | same |
| `Beta.Sessions` | `New(ctx, BetaSessionNewParams, ...)`, `Get(ctx, sessionID, BetaSessionGetParams, ...)`, `Update`, `List(...) (*pagination.BidirectionalPageCursor[BetaManagedAgentsSession], error)`, `ListAutoPaging`, `Delete`, `Archive`; `Resources` (`Add/Get/Update/List/Delete`), `Threads` | same |
| `Beta.Sessions.Events` | `List(ctx, sessionID, BetaSessionEventListParams, ...) (*pagination.PageCursor[BetaManagedAgentsSessionEventUnion], error)`, `ListAutoPaging`, `Send(ctx, sessionID, BetaSessionEventSendParams, ...) (*BetaManagedAgentsSendSessionEvents, error)`, `StreamEvents(ctx, sessionID, BetaSessionEventStreamParams, ...) *ssestream.Stream[BetaManagedAgentsStreamSessionEventsUnion]`, `NewToolRunner` | same signatures; `StreamEvents` resumes |
| `Beta.Files` | `Upload`, `GetMetadata`, `Download`, `List`, `ListAutoPaging`, `Delete` | same |
| `Beta.Skills` (`Versions`), `Beta.Vaults` (`Credentials`, incl. `MCPOAuthValidate`), `Beta.MemoryStores` (`Memories`, `MemoryVersions`), `Beta.UserProfiles`, `Beta.Models` | official | same (BMA serves what its API implements) |

Extensions (no official counterpart; named by the same rules: `New/Get/Update/List/ListAutoPaging/Delete`, path actions in CamelCase, sub-resources as nested services, path parameters positional, one params value):

| Resource | Methods |
|---|---|
| `Beta.Organization.Projects` | `New(ctx, organizationID, OrganizationProjectNewParams, ...) (*Project, error)`, `List(ctx, organizationID, OrganizationProjectListParams, ...) (*Page[Project], error)`, `ListAutoPaging` |
| `Beta.Machines` | `New(ctx, MachineNewParams, ...)`, `Get(ctx, machineID, ...)`, `Update(ctx, machineID, MachineUpdateParams, ...)`, `List(ctx, MachineListParams, ...)`, `ListAutoPaging`, `Delete(ctx, machineID, MachineDeleteParams, ...)`, `Resume(ctx, machineID, ...) (*MachinePowerStatus, error)`, `GetCapabilities(ctx, machineID, ...)` |
| `Beta.MachinePools` | `New`, `Get`, `Update`, `List`, `ListAutoPaging`, `Delete`, `CheckConnection` |
| `Beta.MachinePools.Grants` | `New(ctx, poolID, ...)`, `Get(ctx, poolID, grantID, ...)`, `Update`, `List`, `ListAutoPaging`, `Delete` |
| `Beta.DesktopSessions` | `New`, `Get`, `Close`, `AcquireControl`, `RenewControl`, `ReleaseControl`, `HandbackControl`, `SendActions`, `Screenshot`, `ResumeAgent`, `ConfirmAction(ctx, desktopSessionID, pendingID, ...)` |
| `Beta.DesktopSessions.Tickets` | `New(ctx, desktopSessionID, DesktopSessionTicketNewParams, ...) (*Ticket, error)` (purpose `watch`) |
| `Beta.TerminalSessions` | `New`, `Get`, `List`, `ListAutoPaging`, `Close` |
| `Beta.TerminalSessions.Tickets` | `New(ctx, terminalSessionID, TerminalSessionTicketNewParams, ...) (*Ticket, error)` (purpose `connect`) |

Differences from the official conventions, all in the extensions: optional
fields are pointers (`bmasdk.Ptr`) rather than `param.Opt` (the models come
from oapi-codegen); methods without a query or body take no params value.

## Development

`./tools/generate.sh` regenerates `generated_models.go` (oapi-codegen v2.7.0)
and `generated_resources.go` (`tools/sdkgen/go2gen.py`, resource map
`contracts/bma/v2/sdk.resources.yaml`; an unmapped operation fails). Refresh
the contract from a checkout of beeos-ai/beeos-managed-agents with
`python3 tools/v2/bundle_contract.py --source <checkout>`.

```bash
cd v2 && go vet ./... && go test -race ./...
# live test against staging (creates and removes an environment, agent and session)
BMA_INTEGRATION=1 BMA_API_KEY=… BMA_BASE_URL=https://api.staging.bma.beeos.ai BMA_PROJECT_ID=… BMA_ORG_ID=… \
  go test -run TestStaging -v -timeout 20m ./...
```
