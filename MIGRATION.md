# Migrating to the resource-style SDK

ADR 0012 replaces the path-and-verb calls of bma-sdk 0.4 with resource
methods in TypeScript, Python and Go (one release, **1.0.0**, the same
version in all three).

## All languages

- **Credentials and scope.** The token and base URL default to `BMA_TOKEN`
  and `BMA_BASE_URL`, the organization and project to `BMA_ORG_ID` and
  `BMA_PROJECT_ID`; explicit options win.
- **Base URL is the origin.** `BMA_BASE_URL` and the `baseUrl` / `base_url` /
  `option.WithBaseURL` option are the deployment origin, for example
  `https://api.staging.bma.beeos.ai` (as `ANTHROPIC_BASE_URL` is for the
  Anthropic SDKs); the native client adds `/api/v1` and the facade
  extensions `/v1`, so one value serves both. 0.4 took the API root
  (`https://host/api/v1`): such a value still works, because a trailing
  `/api/v1` is dropped before the prefix is added (no `/api/v1/api/v1`), but
  prefer the origin. `DEFAULT_BASE_URL` / `DefaultBaseURL` changed from
  `https://api.bma.beeos.ai/v1` to the origin `https://api.bma.beeos.ai`,
  which does not resolve yet: set `BMA_BASE_URL`. A base URL ending in `/v1`
  is still rejected by the facade extensions.
- **Timeouts.** 60 s per attempt by default, counted until the response
  arrives. Uploads (binary and multipart bodies) are never cut off while the
  body is being sent: TypeScript applies only a per-call `timeout` to them;
  Go starts the timeout once the body is sent; Python's httpx timeout is per
  phase (connect, write, read). `0` (TypeScript, Go) or `None` (Python)
  disables the timeout. Event streams and downloads are bounded only until
  the headers arrive.
- **Retries.** Two retries; 409 is never retried. An `idempotencyKey` /
  `idempotency_key` / `option.WithIdempotencyKey` on an operation that does
  not declare the `Idempotency-Key` header is an error before any request.
  An upload body that cannot be replayed (a non-seekable stream) is sent once
  and not retried; files and in-memory bodies are resent from their start.
- **Errors.** `error.retryable` is gone: the SDK already retried what is
  retryable; branch on the status class (`ServiceUnavailableError`,
  `*bma.Error.StatusCode`) or the contract `code`.
- **Event streams** behave like EventSource: when the connection drops or the
  server ends the response (for example during a deployment), the stream
  reconnects with `Last-Event-ID` set to the last durable frame and discards
  an unterminated frame. A stream never ends on its own; it stops when you
  close it or raises once the reconnect budget (`maxRetries` / `max_retries`
  / `WithMaxRetries`, counted in a row without receiving data) is spent.
- **Custom tool runner** never stops silently: it reconnects without limit
  by default (`max_reconnects` / `MaxReconnects` bounds it, independently of
  the retry budget), treats a 409 on submit (another consumer answered) as
  handled, and otherwise fails with the error that stopped it.
- **Lists.** Every list whose response is `{data, next_<param>}` pages
  automatically, not only `cursor` lists: also `agents.events.list`
  (`after_sequence`, or `before_sequence` when you pass it),
  `agents.sessions.list` (`before_id`), `agentSessions.list` (`after_id`),
  `agents.turns.list`, `agents.turns.events.list`, `files.list` (`page`) and
  the facade `sessions.files.list`. In Python and Go the page's
  `next_cursor` / `NextCursor` holds the next value of that parameter
  (formerly `next_before_id`, `next_page`, ...).
- **Binary downloads** are named `download` everywhere (`files.download`,
  `agents.artifacts.download`, `agents.sessions.artifacts.download`,
  `memoryStores.files.download`, facade `sessions.files.download`) and
  return the raw response. The artifact helper that checks size and digest
  is `downloadVerified` / `download_verified` / `DownloadVerified`.
- **`agents.create`** returns the 200 body (`CurrentAgentResponse`, a replay
  of an earlier create) or the 201 body (`LaunchAgentResponse`): TypeScript
  `'agent_config' in result`, Python `isinstance`, Go whichever pointer of
  `AgentNewResponse` is set.

## TypeScript

### Client

```ts
// 0.4
const bma = new BmaClient({ token, baseUrl });
const path = { orgID, projectID, agentID };

// now: org and project are client defaults (or BMA_ORG_ID / BMA_PROJECT_ID)
const bma = new BmaClient({ token, baseUrl, orgId, projectId });
```

The package is ESM-only and needs Node.js 20 or newer (as 0.4). Pass
`org_id` / `project_id` in params to address another organization or project
for one call. New options: `timeout` and `maxRetries`; see "All languages".

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
| `bma.downloadArtifact(artifact, { maxBytes })` | `bma.agents.artifacts.downloadVerified(artifact, { maxBytes })` |
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
| list endpoints returning `{data, next_<param>}` | `bma.agents.list()` returns a `SyncCursorPage` (`data`, `next_cursor`); iterating it walks every page |
| `bma.download_artifact(artifact, max_bytes=)` | `bma.agents.artifacts.download_verified(artifact, max_bytes=)` |
| `BmaApiError(status, code)`, `.retryable` | `BmaApiError` subclasses by status (`NotFoundError`, `ConflictError`, ...); the SDK retries |
| `FacadeExtensionsClient(api_key, base_url, project_id=)`, `ext.upload_session_file(id, name, data)` | `FacadeExtensions(api_key=, base_url=, project_id=)`, `ext.sessions.files.upload(id, file=(name, data))` |
| `FacadeApiError` | `ConflictError` etc. with `.type` |
| — | `define_tool(name=, description=, input_model=, run=)` + `bma.agents.tool_calls.runner(agent, tools=[...]).until_done()` |

## Go

Packages `rest` and `facadeext` are removed. The root package `bma` holds
the models (oapi-codegen names, e.g. `bma.Agent`, `bma.CreateAgentInputContentBlock`,
now with Go initialisms: `ID`, `AgentID`, `SessionIDs`, `URL`, `API`, `TTL`, `CPU`,
`JSON` instead of `Id`, `AgentId`, `SessionIds`, `Url`, ...) and the client; options are in `github.com/beeos-ai/bma-sdk/option`; the
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
| `client.DownloadArtifact(ctx, artifact, max, w)` | `client.Agents.Artifacts.DownloadVerified(ctx, artifact, max, w)` |
| `ValueByDiscriminator()` | also `AsAny()` on every discriminated union |
| `facadeext.New(facadeext.Options{...})`, `ext.UploadSessionFile(ctx, id, name, r)` | `facade.NewClient(option.WithAPIKey(k), option.WithBaseURL(origin), option.WithProject(p))`, `ext.Sessions.Files.Upload(ctx, id, facade.SessionFileUploadParams{File: bma.NewFile(r, name)})` |
| `createAgent` 200/201 in `JSON200`/`JSON201` | `client.Agents.New` returns `*bma.AgentNewResponse` with `CurrentAgentResponse` (200, replay) or `LaunchAgentResponse` (201) set |
| — | `bma.DefineTool(name, description, inputSchema, fn)` + `client.Agents.ToolCalls.Runner(agentID, params).Run(ctx)` |

Machine Daemon operations (bmad) have no resource method in Python and Go;
they stay in the TypeScript `bma.rest` escape hatch only.
