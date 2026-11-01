# BMA SDKs

Go, TypeScript and Python SDKs for BMA (BeeOS Managed Agents), generated from
the BMA contracts in [`contracts/bma/`](contracts/bma). Two SDK families live
in this repository and version independently:

- **bma-sdk**: for applications that call the BMA API. Typed clients for the
  native REST API (`rest.openapi.yaml`) and the BMA extensions to the
  Anthropic Managed Agents façade (`facade-extensions.openapi.yaml`).
- **bma-executor-sdk**: for programs that execute work for BMA or drive an
  executor. The executor, harness and agent ends of the Executor Protocol
  `bma.executor.v1.1`, with types generated from
  [`contracts/bma/executor/`](contracts/bma/executor).

## Versions and installation

| Family | Language | Package | Version | Install |
| --- | --- | --- | --- | --- |
| bma-sdk | Go | [![Go Reference](https://pkg.go.dev/badge/github.com/beeos-ai/bma-sdks/go.svg)](https://pkg.go.dev/github.com/beeos-ai/bma-sdks/go) `github.com/beeos-ai/bma-sdks/go` | 0.4.0 (`go/v0.4.0`) | `go get github.com/beeos-ai/bma-sdks/go@v0.4.0` |
| bma-sdk | TypeScript | [![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk) [`@beeos-ai/bma-sdk`](typescript) | 0.4.0 (`ts/v0.4.0`) | `npm install @beeos-ai/bma-sdk@0.4.0` |
| bma-sdk | Python | [![PyPI](https://img.shields.io/pypi/v/bma-sdk.svg)](https://pypi.org/project/bma-sdk/) [`bma-sdk`](python) | 0.4.0 (`python/v0.4.0`) | `pip install bma-sdk==0.4.0` |
| bma-executor-sdk | Go | [![Go Reference](https://pkg.go.dev/badge/github.com/beeos-ai/bma-sdks/executor.svg)](https://pkg.go.dev/github.com/beeos-ai/bma-sdks/executor) [`github.com/beeos-ai/bma-sdks/executor`](executor) | 0.4.8 (`executor/v0.4.8`) | `go get github.com/beeos-ai/bma-sdks/executor@v0.4.8` |
| bma-executor-sdk | TypeScript | [![npm](https://img.shields.io/npm/v/@beeos-ai/bma-executor-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-executor-sdk) [`@beeos-ai/bma-executor-sdk`](executor/typescript) | 0.4.8 (`executor-ts/v0.4.8`) | `npm install @beeos-ai/bma-executor-sdk@0.4.8` |
| bma-executor-sdk | Python | [![PyPI](https://img.shields.io/pypi/v/bma-executor-sdk.svg)](https://pypi.org/project/bma-executor-sdk/) [`bma-executor-sdk`](executor/python) | 0.4.8 (`executor-python/v0.4.8`) | `pip install bma-executor-sdk==0.4.8` |

| Compatibility | bma-sdk 0.4.0 | bma-executor-sdk 0.4.8 |
| --- | --- | --- |
| BMA contract | REST and façade at BMA commit `ceee7dcf` ([`contracts/bma/lock.json`](contracts/bma/lock.json)) | Executor contract 1.1.0 at BMA commit `69c05b65` ([`contracts/bma/executor/lock.json`](contracts/bma/executor/lock.json)) |
| Protocol | BMA REST `/api/v1` and the Anthropic Managed Agents façade extensions | `bma.executor.v1.1` (harness also accepts `bma.executor.v1`) |
| Go | 1.24+ | 1.24+ |
| Node.js | 20+ (ESM) | 20+ (ESM) |
| Python | 3.10+ | 3.10+ |

Release notes: [CHANGELOG](CHANGELOG.md) and
[GitHub Releases](https://github.com/beeos-ai/bma-sdks/releases).

| Read next | |
| --- | --- |
| Call the BMA API | [REST quick start](#rest-quick-start) below; [TypeScript](typescript/README.md), [Python](python/README.md) |
| Write or drive an executor | [Executor integration guide](docs/executor/README.md) ([中文](docs/executor/README.zh-CN.md)); package READMEs for [Go](executor/README.md), [TypeScript](executor/typescript/README.md), [Python](executor/python/README.md) |

## Packages

| SDK | Package | Purpose |
| --- | --- | --- |
| Go | `github.com/beeos-ai/bma-sdks/go/rest` | Every operation in `rest.openapi.yaml`: agents, agent sessions (create/get/list/update/archive, session model override incl. `expires_with_session`), inputs and events with `session_id`, the SSE stream, artifacts, machines, desktop and terminal sessions and connection tickets, configuration. |
| Go | `github.com/beeos-ai/bma-sdks/go/facadeext` | BMA extensions to the Anthropic facade: `/v1/sessions/{id}/desktop/stream`, `/v1/sessions/{id}/files` upload/list, and the `bma_sequence`, `Idempotency-Key`, `mcp_servers[].bma_auth` and model-override field types. |
| Go | [`github.com/beeos-ai/bma-sdks/executor`](executor) (separate module) | Executor end (`Client`), execution core (`Core`: bash, file tools, stdio MCP, `process.*` and `skill.install` capabilities), harness end (`Harness`) and the agent capability; WebSocket, Unix socket and in-process transports. |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | Typed REST client (`.`) and facade extensions (`./facade-extensions`). |
| TypeScript | [`@beeos-ai/bma-executor-sdk`](executor/typescript) | Executor, harness and agent ends of `bma.executor.v1.1` with generated types; WebSocket, WebSocket over a Unix socket or named pipe (`unix://`, `npipe://`), and in-process transports. |
| Python | [`bma-sdk`](python) | `bma_sdk.rest` (generated), `bma_sdk.BmaClient`, `bma_sdk.facade_extensions`. |
| Python | [`bma-executor-sdk`](executor/python) (`bma_executor_sdk`) | `bma.executor.v1.1` executor, harness and agent ends on asyncio; WebSocket, WebSocket over a Unix domain socket, and in-process transports. |

The standard Anthropic facade routes (`/v1/agents`, `/v1/environments`,
`/v1/sessions`, events, events/stream, `/v1/memory_stores`) are intentionally
not wrapped: use the official Anthropic SDKs with `base_url` set to the BMA
facade, and these packages only for what BMA adds.

Neither the native API nor executor protocol v1 has an artifact upload
endpoint. Files a caller supplies are uploaded through the facade extension
`POST /v1/sessions/{id}/files`; artifacts the agent produces are downloaded
with `DownloadArtifact`/`downloadArtifact`/`download_artifact`, which verify
size and sha256.

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

## Executor Protocol

The Executor Protocol connects a harness ("brain": the BMA platform or your
local agent) with executors ("hands" that run tools, processes and MCP
servers). Start with the [integration guide](docs/executor/README.md)
([中文](docs/executor/README.zh-CN.md)):

| I want to | Start here |
| --- | --- |
| Understand roles, deployment shapes and what is available | [Overview](docs/executor/README.md) ([中文](docs/executor/README.zh-CN.md)) |
| Write an executor (a "hand" the BMA cloud or a local brain drives) | [Quick start](docs/executor/quickstart.md) ([中文](docs/executor/quickstart.zh-CN.md)), then the [protocol reference](docs/executor/protocol-reference.md) ([中文](docs/executor/protocol-reference.zh-CN.md)) |
| Drive an executor (be the harness / local brain) | [Local connection and auth](docs/executor/local-connection.md) ([中文](docs/executor/local-connection.zh-CN.md)) and `Harness` in the package READMEs |
| Connect a full local agent (turns in, agent events out) | [Agent capability](docs/executor/agent-capability.md) ([中文](docs/executor/agent-capability.zh-CN.md)) |

API documentation and runnable examples per language:

| Language | README | Examples |
| --- | --- | --- |
| Go | [`executor/README.md`](executor/README.md) | [`executor/examples`](executor/examples): `local-brain`, `cloud-hand`, `agentexecutor`, `echo-mcp` |
| TypeScript | [`executor/typescript/README.md`](executor/typescript/README.md) | [`executor/typescript/examples`](executor/typescript/examples): `executor-minimal`, `harness-loopback`, `agent-minimal` |
| Python | [`executor/python/README.md`](executor/python/README.md) | [`executor/python/examples`](executor/python/examples): `executor_minimal.py`, `harness_loopback.py`, `agent_minimal.py` |

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
