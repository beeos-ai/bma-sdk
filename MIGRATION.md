# Migrating to the resource-style SDK

ADR 0012 replaces the path-and-verb calls of bma-sdk 0.4 with resource
methods. This page covers TypeScript; Python and Go follow in the same
release.

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
