# bma-sdk

Go, TypeScript and Python SDKs for the BMA (BeeOS Managed Agents) API,
generated from the BMA contracts in [`contracts/bma/`](contracts/bma): typed
clients for the native REST API (`rest.openapi.yaml`) and the BMA extensions to
the Anthropic Managed Agents façade (`facade-extensions.openapi.yaml`).

> Moved from [`beeos-ai/bma-sdks`](https://github.com/beeos-ai/bma-sdks) (archived) in 0.4.2.
> The Go import path changed from `github.com/beeos-ai/bma-sdk/...` to
> `github.com/beeos-ai/bma-sdk/...`; the npm and PyPI package names are unchanged.
> The Executor Protocol SDK (executor, harness and agent ends) is
> [`beeos-ai/bma-executor-sdk`](https://github.com/beeos-ai/bma-executor-sdk).

## Versions and installation

| Language | Package | Install |
| --- | --- | --- |
| Go | [![Go Reference](https://pkg.go.dev/badge/github.com/beeos-ai/bma-sdk.svg)](https://pkg.go.dev/github.com/beeos-ai/bma-sdk) `github.com/beeos-ai/bma-sdk` | `go get github.com/beeos-ai/bma-sdk@v0.4.2` |
| TypeScript | [![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk) [`@beeos-ai/bma-sdk`](typescript) | `npm install @beeos-ai/bma-sdk@0.4.2` |
| Python | [![PyPI](https://img.shields.io/pypi/v/bma-sdk.svg)](https://pypi.org/project/bma-sdk/) [`bma-sdk`](python) | `pip install bma-sdk==0.4.2` |

| Compatibility | bma-sdk 0.4.2 (tag `v0.4.2`, all three languages) |
| --- | --- |
| BMA contract | REST and façade at BMA commit `db2403f9` ([`contracts/bma/lock.json`](contracts/bma/lock.json)) |
| Protocol | BMA REST `/api/v1` and the Anthropic Managed Agents façade extensions |
| Runtimes | Go 1.24+, Node.js 20+ (ESM), Python 3.10+ |

Release notes: [CHANGELOG](CHANGELOG.md) and
[GitHub Releases](https://github.com/beeos-ai/bma-sdk/releases).

## Packages

| SDK | Package | Purpose |
| --- | --- | --- |
| Go | `github.com/beeos-ai/bma-sdk` (package `bma`), options in `.../option` | Native REST client: `bma.NewClient(...)` with resources such as `client.Agents.Sessions.New`. |
| Go | `github.com/beeos-ai/bma-sdk/facade` | BMA extensions to the Anthropic facade (session files, resources, desktop stream) and `EventBMASequence`. |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | `BmaClient` (`.`) and `FacadeExtensionsClient` (`./facade-extensions`). |
| Python | [`bma-sdk`](python) | `Bma` / `AsyncBma`, `bma_sdk.types`, `bma_sdk.facade_extensions`. |

All three are resource-style clients (ADR 0012): methods are named in
[`contracts/bma/sdk.resources.yaml`](contracts/bma/sdk.resources.yaml), path
IDs are positional, query/header/body fields form one params value; the
organization and project are client defaults (`BMA_ORG_ID`,
`BMA_PROJECT_ID`) that one call can override, and the token and base URL
default to `BMA_TOKEN` and `BMA_BASE_URL`. Every SDK retries reads and
calls that accept an `Idempotency-Key` (408/429/5xx and connection errors,
with a generated key reused across attempts), other writes only on 429/503 and
requests that never reached the server, never 409, and never a body it cannot
replay; defaults are 2 retries and a 60 s timeout per attempt until the
response arrives (uploads are not cut off while sending; `0` / `None`
disables the timeout). Every `{data, next_<param>}` list pages automatically;
the event stream yields frames discriminated by their SSE event name and,
like EventSource, reconnects from the last durable frame when the connection
drops, the server ends the response or sends `service_unavailable`; errors
carry the HTTP status and the contract's `ErrorCode`. See
[MIGRATION.md](MIGRATION.md) for 0.4 code.

The standard Anthropic facade routes (`/v1/agents`, `/v1/environments`,
`/v1/sessions`, events, events/stream, `/v1/memory_stores`) are intentionally
not wrapped: use the official Anthropic SDKs with `base_url` set to the BMA
facade, and these packages only for what BMA adds.

## REST quick start

Set `BMA_BASE_URL` to the origin of your deployment, for example
`https://api.staging.bma.beeos.ai` (the default `https://api.bma.beeos.ai`
does not resolve yet), `BMA_TOKEN`, `BMA_ORG_ID` and `BMA_PROJECT_ID`, or
pass them as options. Like `ANTHROPIC_BASE_URL`, the base URL is an origin:
the native client adds `/api/v1` and the facade extensions `/v1` (a value
already ending in `/api/v1` is accepted, not doubled).

Go:

```go
client := bma.NewClient() // or option.WithBaseURL, WithToken, WithOrg, WithProject
created, err := client.Agents.Sessions.New(ctx, agentID, bma.AgentSessionNewParams{IdempotencyKey: bma.Ptr("task-1")})
if err != nil {
	log.Fatal(err)
}
_, err = client.Agents.Inputs.New(ctx, agentID, bma.AgentInputNewParams{
	SessionID:     bma.Ptr(created.Session.ID),
	ContentBlocks: []bma.CreateAgentInputContentBlock{bma.NewTextInputBlock("Start the task.")},
})
if err != nil {
	log.Fatal(err)
}
stream := client.Agents.Events.Stream(ctx, agentID, bma.AgentEventStreamParams{SessionID: bma.Ptr(created.Session.ID)})
defer stream.Close()
for stream.Next() {
	switch ev := stream.Current().AsAny().(type) {
	case bma.ModelOutputEvent:
		log.Printf("model output %d", ev.Sequence)
	case bma.ToolCallUpdate:
		log.Printf("tool call %s is %s", ev.ToolCallID, ev.State)
	}
}
var apiErr *bma.Error
if err := stream.Err(); errors.As(err, &apiErr) {
	log.Printf("%d %s", apiErr.StatusCode, apiErr.Code)
}

pager := client.Agents.ListAutoPaging(ctx, bma.AgentListParams{})
for pager.Next() {
	log.Println(pager.Current().ID)
}
```

TypeScript:

```ts
const bma = new BmaClient(); // or { baseUrl, token, orgId, projectId }
const { session } = await bma.agents.sessions.create(agentId, { idempotency_key: "task-1" });
await bma.agents.inputs.create(agentId, { session_id: session.id, content_blocks: [{ type: "text", text: "Start the task." }] });
for await (const ev of bma.agents.events.stream(agentId, { session_id: session.id })) {
  if (ev.event === "model_output") console.log(ev.sequence, ev.data.content_blocks);
}
for await (const agent of bma.agents.list()) console.log(agent.id);
```

Python:

```python
bma = Bma()  # or Bma(token=, base_url=, org_id=, project_id=)
created = bma.agents.sessions.create(agent_id, idempotency_key="task-1")
bma.agents.inputs.create(agent_id, session_id=created.session.id,
                         content_blocks=[{"type": "text", "text": "Start the task."}])
for ev in bma.agents.events.stream(agent_id, session_id=created.session.id):
    if ev.event == "model_output":
        print(ev.sequence, ev.data.content_blocks)
for agent in bma.agents.list():
    print(agent.id)
```

### Files: upload, mount, outputs

A project file is uploaded once and mounted into sessions by reference. The
machine executor mirrors the mounts below `/mnt/session/uploads` (read-only)
and uploads what the agent writes to `/mnt/session/outputs` back into the
session's scope, so listing files with `scope_id=<session>` returns the
session's outputs.

```go
file, err := client.Files.Upload(ctx, bma.FileUploadParams{Filename: "report.pdf", Body: reader})
mounted, err := client.Agents.Sessions.Resources.Add(ctx, agentID, sessionID, bma.AgentSessionResourceAddParams{
	Type: bma.FileResourceParamsTypeFile, FileID: file.ID, MountPath: bma.Ptr("/mnt/session/uploads/reports/report.pdf"),
})
outputs, err := client.Files.List(ctx, bma.FileListParams{ScopeID: bma.Ptr(sessionID)})
```

```ts
const file = await bma.files.upload({ filename: "report.pdf", body: await readFile("report.pdf") });
await bma.agents.sessions.resources.add(agentId, sessionId, { type: "file", file_id: file.id, mount_path: "/mnt/session/uploads/reports/report.pdf" });
const outputs = await bma.files.list({ scope_id: sessionId });
```

```python
file = bma.files.upload(filename="report.pdf", body=Path("report.pdf").read_bytes())
bma.agents.sessions.resources.add(agent_id, session_id, type="file", file_id=file.id,
                                  mount_path="/mnt/session/uploads/reports/report.pdf")
outputs = bma.files.list(scope_id=session_id)
```

Artifacts the agent produces are downloaded with
`client.Agents.Artifacts.DownloadVerified` / `bma.agents.artifacts.downloadVerified` /
`bma.agents.artifacts.download_verified`, which verify the recorded size and
sha256; `download` returns the raw content.

## Development

```bash
./tools/generate.sh                                  # regenerate Go, TypeScript and Python
uv run --no-project --with pyyaml --with jsonschema \
  python tools/check_contract.py [--source ../beeos-managed-agents]
go vet ./... && go test -race ./...
(cd typescript && npm ci && npm run build && npm test)
(cd python && uv run pytest -q && uv run pyright)
```

`tools/generate.sh` needs Python 3 with PyYAML, Go 1.24+, Node 20+ and uv; it
pins oapi-codegen v2.7.0 (Go models), openapi-typescript 7.13.0 (TypeScript
types) and ruff (formatting of the Python output); the resource layers and the
Python models come from [`tools/sdkgen`](tools/sdkgen). Never edit generated
files by hand. The SDK tests of all three
languages replay the same recorded exchanges in
[`contracts/bma/fixtures/sdk-contract.json`](contracts/bma/fixtures/sdk-contract.json),
which `tools/check_contract.py` validates against the contracts. See
[`contracts/bma/README.md`](contracts/bma/README.md) for refreshing the
contract.

`go test -run TestStagingSmoke .` runs the staging smoke (creates an agent
with a custom tool, answers it with the tool runner, archives the agent) when `BMA_BASE_URL`, `BMA_ORG_API_KEY`, `BMA_ORG_ID` and
`BMA_PROJECT_ID` are set; otherwise it is skipped.

## Release

One tag `v<version>` releases all three languages at the same version: it must
be on `main`, and [`tools/check_versions.sh`](tools/check_versions.sh) checks it
against `typescript/package.json`, `python/pyproject.toml` (the Python client
reads its version from the installed metadata) and the User-Agent constants
`typescript/src/version.ts` and `client.go` (CI runs the same check without a tag).
[`release.yaml`](.github/workflows/release.yaml) first runs
[`ci.yaml`](.github/workflows/ci.yaml) (regenerate every SDK with no diff,
contract drift check, Go, TypeScript and Python tests), then publishes.

| Channel | Publishes | Credentials |
| --- | --- | --- |
| Go | nothing; the module comes from the tag | none |
| npm | `@beeos-ai/bma-sdk` with provenance | secret `NPM_TOKEN` in the `releases` environment |
| PyPI | `bma-sdk` | a PyPI Trusted Publisher on `bma-sdk`: owner `beeos-ai`, repository `bma-sdk`, workflow `release.yaml`, environment `releases` |

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
