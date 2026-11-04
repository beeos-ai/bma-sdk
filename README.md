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
| Go | `github.com/beeos-ai/bma-sdk/rest` | Every operation in `rest.openapi.yaml`: agents, agent sessions (create/get/list/update/archive, session model override incl. `expires_with_session`), inputs and events with `session_id`, the SSE stream, artifacts, machines, desktop and terminal sessions and connection tickets, configuration. |
| Go | `github.com/beeos-ai/bma-sdk/facadeext` | BMA extensions to the Anthropic facade: `/v1/sessions/{id}/desktop/stream`, `/v1/sessions/{id}/files` upload/list, and the `bma_sequence`, `Idempotency-Key`, `mcp_servers[].bma_auth` and model-override field types. |
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

## REST quick start

`rest/generated.go` is generated from the contract; only authentication,
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

	bmarest "github.com/beeos-ai/bma-sdk/rest"
)

func main() {
	client, err := bmarest.New(bmarest.Options{
		BaseURL: os.Getenv("BMA_BASE_URL"), // required: see below
		Token:   os.Getenv("BMA_TOKEN"),
	})
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

Set `Options.BaseURL` to your BMA deployment: the hosted service is in early
access and the default `DefaultBaseURL` (`https://api.bma.beeos.ai/v1`) does
not resolve yet. It is the API root including `/v1` (for example
`https://bma.example.com/api/v1` when the API is served under `/api`). The SDK
does not read `BMA_BASE_URL` itself; the example passes it through. The facade
extensions client (`facadeext.Options.BaseURL`) has no default and takes the
facade origin without `/v1`.

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

## Development

```bash
./tools/generate.sh                                  # regenerate Go, TypeScript and Python
uv run --no-project --with pyyaml --with jsonschema \
  python tools/check_contract.py [--source ../beeos-managed-agents]
go vet ./... && go test -race ./...
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

One tag `v<version>` releases all three languages at the same version: it must
be on `main` and match `typescript/package.json` and `python/pyproject.toml`.
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
