# Migrating to the resource-style SDK

ADR 0012 replaces the path-and-verb calls of bma-sdk 0.4 with resource
methods in TypeScript, Python and Go (one release, 1.0.0).

## TypeScript

### Client

```ts
// 0.4
const bma = new BmaClient({ token, baseUrl });
const path = { orgID, projectID, agentID };

// now: org and project are client defaults (or BMA_ORG_ID / BMA_PROJECT_ID)
const bma = new BmaClient({ token, baseUrl, orgId, projectId });
```

Pass `org_id` / `project_id` in params to address another organization or
project for one call. New options: `timeout` (60 s per attempt) and
`maxRetries` (2); see the README for the retry rules.

### Calls

| 0.4 | now |
| --- | --- |
| `unwrap(await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/sessions", { params: { path }, body }))` | `await bma.agents.sessions.create(agentId, body)` |
| `unwrap(await bma.rest.GET(".../agents/{agentID}/sessions/{sessionID}", { params: { path } }))` | `await bma.agents.sessions.retrieve(agentId, sessionId)` |
| `bma.rest.POST(".../inputs", { params: { path, query: { session_id }, header: { "Idempotency-Key": k } }, body })` | `bma.agents.inputs.create(agentId, { session_id, ...body }, { idempotencyKey: k })` |
| `bma.rest.GET(".../agents", { params: { path, query: { cursor, limit } } })` | `await bma.agents.list({ limit })` (first page) or `for await (const a of bma.agents.list())` (all) |
| `bma.streamEvents({ orgID, projectID, agentID, sessionId, afterSequence, lastEventId, streamDeltas })` | `bma.agents.events.stream(agentId, { session_id, after_sequence, last_event_id, stream_deltas })` |
| `frame.event: string`, `frame.data: AgentEventStreamData` | `ev.event` narrows `ev.data` (`model_output` → `ModelOutputEvent`, ...) |
| a frame with `event === "error"` | not yielded: `service_unavailable` reconnects, any other code throws `EventStreamError` |
| `bma.downloadArtifact(artifact, { maxBytes })` | `bma.agents.artifacts.download(artifact, { maxBytes })` |
| `bma.rest.POST(".../files", { body, bodySerializer, headers: { "Content-Type": ... } })` | `bma.files.upload({ filename, body })` |
| `Schemas["AgentSession"]` | `AgentSession` (every schema is exported by name) |

The full method list is [`contracts/bma/sdk.resources.yaml`](contracts/bma/sdk.resources.yaml)
(operationId → `resource.method`). Params keep the wire field names
(snake_case).

### Errors

| 0.4 | now |
| --- | --- |
| `BmaApiError` with `status`, `code: string` | `BmaApiError` subclasses by status (`NotFoundError`, `ConflictError`, `RateLimitError`, ...) with `code: ErrorCode` |
| `error.retryable` | removed; the SDK retries (README, "Errors, retries, timeouts") |
| `FacadeApiError` | the same `BmaApiError` subclasses; `error.type` holds the facade `error.type` |

### Facade extensions

| 0.4 | now |
| --- | --- |
| `ext.getSessionDesktopStream(id, { desktopSessionId, ttlSeconds, origin })` | `ext.sessions.desktop.stream(id, { desktop_session_id, ttl_seconds, origin })` |
| `ext.uploadSessionFile(id, blob, filename)` | `ext.sessions.files.upload(id, { file: new File([blob], filename) })` |
| `ext.listSessionFiles(id, { limit, page })` | `ext.sessions.files.list(id, { limit, page })` |
| `ext.downloadSessionFile(id, fileId)` → `{ content, contentType, filename, digest }` | `ext.sessions.files.download(id, fileId)` → `Response` (`x-bma-file-digest`, `content-disposition` headers) |
| `ext.addSessionResource(id, fileId, mountPath)` | `ext.sessions.resources.add(id, { type: "file", file_id, mount_path })` |
| `ext.listSessionResources(id)` / `ext.deleteSessionResource(id, rid)` | `ext.sessions.resources.list(id)` / `ext.sessions.resources.delete(id, rid)` |
| `ext.raw`, `IDEMPOTENCY_KEY_HEADER` | removed |

### Escape hatch

`bma.rest` (openapi-fetch, typed by contract path) and `unwrap()` remain for
operations without a resource method: the Machine Daemon routes used by bmad
and the desktop signaling WebSocket. `unwrap` now throws the status
subclasses.

### Removed

`BmaClient.streamEvents`, `BmaClient.downloadArtifact`, `parseSSE`,
`StreamFrame`, `StreamEventsOptions`, `Schemas`, the facade method names
above, `FacadeApiError`.

## Python

The openapi-python-client layer (`bma_sdk.rest.api.*`, attrs models,
`unwrap`) is replaced by resource methods with keyword arguments, pydantic v2
response models and TypedDict request types (`bma_sdk.types`). New runtime
dependency: `pydantic>=2.7` (attrs and python-dateutil are gone).

```python
# 0.4
bma = BmaClient(token, base_url)
created = unwrap(create_agent_session.sync_detailed(org, project, agent, client=bma.rest,
                 body=CreateAgentSessionRequest(idempotency_key="task-1")))

# now: org and project are client defaults (or BMA_ORG_ID / BMA_PROJECT_ID)
bma = Bma(token=token, base_url=base_url, org_id=org, project_id=project)
created = bma.agents.sessions.create(agent, idempotency_key="task-1")
```

| 0.4 | now |
| --- | --- |
| `BmaClient(token, base_url)` | `Bma(token=, base_url=, org_id=, project_id=)`; `AsyncBma` for asyncio |
| `unwrap(<op>.sync_detailed(org, project, ..., client=bma.rest, body=Model(...)))` | `bma.<resource>.<method>(ids..., field=value, ...)`; `org_id=` / `project_id=` override the defaults |
| `TextContentBlock(type_="text", text=...)` (attrs) | `{"type": "text", "text": ...}` (TypedDict `TextContentBlockParam`) |
| `UNSET` | omit the argument (`NOT_GIVEN`); `None` sends JSON null |
| response attrs models (`type_`, `additional_properties`) | pydantic models from `bma_sdk.types` (`type`, extra fields kept); `.to_dict()`, `.to_json()` |
| `bma.stream_events(org, project, agent, ...)` → `StreamFrame(event, data: dict)` | `bma.agents.events.stream(agent, session_id=..., last_event_id=...)`; `ev.event` narrows `ev.data` |
| list endpoints returning `{data, next_cursor}` | `bma.agents.list()` returns a `SyncCursorPage`; iterating it walks every page |
| `bma.download_artifact(artifact, max_bytes=)` | `bma.agents.artifacts.download(artifact, max_bytes=)` |
| `BmaApiError(status, code)`, `.retryable` | `BmaApiError` subclasses by status (`NotFoundError`, `ConflictError`, ...); the SDK retries |
| `FacadeExtensionsClient(api_key, base_url, project_id=)`, `ext.upload_session_file(id, name, data)` | `FacadeExtensions(api_key=, base_url=, project_id=)`, `ext.sessions.files.upload(id, file=(name, data))` |
| `FacadeApiError` | `ConflictError` etc. with `.type` |
| — | `define_tool(name=, description=, input_model=, run=)` + `bma.agents.tool_calls.runner(agent, tools=[...]).until_done()` |

## Go

Packages `rest` and `facadeext` are removed. The root package `bma` holds
the models (same oapi-codegen names, e.g. `bma.Agent`, `bma.CreateAgentInputContentBlock`)
and the client; options are in `github.com/beeos-ai/bma-sdk/option`; the
facade extensions are package `github.com/beeos-ai/bma-sdk/facade`.

```go
// 0.4
client, err := bmarest.New(bmarest.Options{BaseURL: base, Token: token})
resp, err := client.CreateAgentSessionWithResponse(ctx, org, project, agentID, bmarest.CreateAgentSessionJSONRequestBody{...})
if err := bmarest.CheckResponse(resp.HTTPResponse, resp.Body); err != nil { ... }
session := resp.JSON201.Session

// now
client := bma.NewClient(option.WithBaseURL(base), option.WithToken(token), option.WithOrg(org), option.WithProject(project))
created, err := client.Agents.Sessions.New(ctx, agentID, bma.AgentSessionNewParams{IdempotencyKey: bma.Ptr("task-1")})
session := created.Session
```

| 0.4 | now |
| --- | --- |
| `bmarest.New(bmarest.Options{...})` | `bma.NewClient(option.With...)`; `option.WithProject(p)` per call overrides the scope |
| `client.XxxWithResponse(ctx, org, project, ids..., &XxxParams{...}, XxxJSONRequestBody{...})` + `CheckResponse` + `resp.JSON200` | `client.<Resource>.<Method>(ctx, ids..., bma.<Resource><Method>Params{...})` returns the body type and `error`; query, header and body fields are one flat struct |
| `&bmarest.XxxParams{IdempotencyKey: ...}` | `option.WithIdempotencyKey(k)`; generated and reused across retries when omitted |
| `*bmarest.APIError`, `bmarest.ErrorCode` strings | `*bma.Error` (`errors.As`), `Code bma.ErrorCode` with the generated `bma.ErrorCode...` constants |
| `client.OpenEventStream(...)` + `stream.Next() (StreamFrame, error)` | `stream := client.Agents.Events.Stream(ctx, agentID, params)`; `for stream.Next() { switch v := stream.Current().AsAny().(type) { case bma.ModelOutputEvent: ... } }`; `stream.Err()` |
| list + manual cursor | `List` (one page, `HasNextPage`/`GetNextPage`) and `ListAutoPaging` (`Next`/`Current`/`Err`) |
| `client.DownloadArtifact(ctx, artifact, max, w)` | `client.Agents.Artifacts.Download(ctx, artifact, max, w)` |
| `ValueByDiscriminator()` | also `AsAny()` on every discriminated union |
| `facadeext.New(facadeext.Options{...})`, `ext.UploadSessionFile(ctx, id, name, r)` | `facade.NewClient(option.WithAPIKey(k), option.WithBaseURL(origin), option.WithProject(p))`, `ext.Sessions.Files.Upload(ctx, id, facade.SessionFileUploadParams{File: bma.NewFile(r, name)})` |
| `createAgent` 200/201 in `JSON200`/`JSON201` | `client.Agents.New` returns `*bma.AgentNewResponse` with `CurrentAgentResponse` (200, replay) or `LaunchAgentResponse` (201) set |
| — | `bma.DefineTool(name, description, inputSchema, fn)` + `client.Agents.ToolCalls.Runner(agentID, params).Run(ctx)` |

Machine Daemon operations (bmad) have no resource method in Python and Go;
they stay in the TypeScript `bma.rest` escape hatch only.
