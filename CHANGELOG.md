# Changelog

## Unreleased: 2.x

Wire default of the project scope (ADR 0032, S-W3 first step; no API change):

- Go `v2` `WithProject`, TypeScript `project` / `BMA_PROJECT_ID`, Python `project=` / `BMA_PROJECT_ID`
  now send `bma-workspace-id` instead of `x-bma-project-id` (same value, only the header name).
  The server accepts both; `x-bma-project-id` is a transition alias that is removed after its
  counter stays at 0. A client sends one scope header, so it never conflicts with itself.
  Servers older than ADR 0032 (no `bma-workspace-id`) ignore the new header, so a multi-project key
  needs the option `default_headers` / `WithHeader` with the old name there.
- Option and environment names (`project`, `WithProject`, `BMA_PROJECT_ID`) are unchanged; the
  rename to workspace options is the 3.0.0 work.
- Go 1.x (root module) is frozen and unchanged.

## 2.1.0 (Go, TypeScript, Python)

Additive release, no breaking change. v2.1.0 releases Go (`github.com/beeos-ai/bma-sdk/v2`,
directory `v2/`), npm `@beeos-ai/bma-sdk` and PyPI `bma-sdk` together.

New:

- `sessions.events.sendAndStream` / `SendAndStream` / `send_and_stream`:
  sends, then opens the resuming stream at the `bma_resume_cursor` of the send
  response (the session's last sequence before the send), so frames an
  executor wrote before the subscribe are not lost; a reconnect before the
  first durable frame reuses the cursor. No cursor for a `user.message`:
  starts at `Last-Event-ID: 0` and reports `Replayed`; no `user.message` in
  the send: server default position.

## 2.0.0 (Go, TypeScript, Python)

New major version of all three SDKs (ADR 0025), released as v2.0.0. See
MIGRATION.md and each language's README.

Each SDK is the official Anthropic SDK plus the BMA extensions:

- The shared Claude Managed Agents resources (`client.beta.agents`,
  `environments`, `sessions`, `sessions.events`, `files`, `skills`, `vaults`,
  `memoryStores`, …) are the official services with their signatures:
  anthropic-sdk-go v2.7.0 (Go), `@anthropic-ai/sdk` 1.6.0 (TypeScript, `BmaClient`
  extends `Anthropic`), `anthropic` 2.6.0 (Python, `Bma` / `AsyncBma` subclass
  `Anthropic` / `AsyncAnthropic`).
- BMA extensions generated from `contracts/bma/v2/extensions.openapi.yaml`
  (generators `tools/sdkgen/{go2gen,ts2gen,py2gen}.py`, one resource map):
  `beta.organization.projects`, `beta.machines`, `beta.machinePools` (`.grants`),
  `beta.desktopSessions` (`.tickets`), `beta.terminalSessions` (`.tickets`).
  Deprecated extension routes (`/orgs/{org_id}/projects`, `watch_tickets`,
  `connection_tickets`) are not included.
- Typed `bma_*` fields: accessors for responses (`SessionExtensions` /
  `sessionExtensions` / `session_extensions`, agent, environment, event) and
  typed request fields or options (`bma_model_override` incl. revoke,
  `bma_harness`, `bma_desktop`).
- `sessions.events.stream` keeps the official signature and resumes a dropped
  stream with `Last-Event-ID` (the `bma_sequence` before the last frame's;
  frames already returned are skipped by id), up to 5 attempts in a row with
  backoff 0.5–8 s.
- Extension creates send an automatic `Idempotency-Key` (one per call, reused
  by retries); `project` / `WithProject` sets `x-bma-project-id`.
- Errors are the official classes; `ErrorCode` / `errorCode` / `error_code`
  return BMA's `error.code`.
- Credentials from `BMA_API_KEY` / `BMA_BASE_URL` / `BMA_PROJECT_ID`; the
  `ANTHROPIC_*` environment and the official credential profiles are never read.
- Minimum runtimes: Go 1.25 (2.0 module; required by the official v2), Node.js 20,
  Python 3.10 (unchanged for TypeScript and Python).
- TypeScript and Python 2.0 replace the 1.x clients in `typescript/` and
  `python/` (1.x stays on the npm and PyPI registries and at tag `v1.0.1`); the
  Go 1.x module at the repository root is frozen.
- `tools/check_versions.sh` and `release.yaml` cover the three 2.0 packages;
  staging tests in all three languages (`BMA_INTEGRATION=1`).

## Unreleased: 1.x

Toolchain and dependency upgrade; no API change and no change to the minimum
supported runtimes (Go 1.24, Node.js 20, Python 3.10).

- **CI:** matrix of the oldest supported runtimes (Go 1.24, Node 20,
  Python 3.10), Go 1.26 / Node 24 / Python 3.13, and Go 1.27 / Node 26 /
  Python 3.14; the release job publishes npm with Node 26. GitHub Actions are
  pinned by commit SHA at their latest stable release.
- **Runtime dependencies:** already at their latest stable versions
  (`oapi-codegen/runtime` 1.8.0, `openapi-fetch` 0.17.0); Python ranges
  unchanged.
- **Generators:** ruff 0.14.4 → 0.17.4 (no generated diff).
  oapi-codegen stays at v2.7.0: v2.8 renames Go enum constants
  (`Active` → `AgentSessionStateActive`), a breaking change for Go users.
- **Development only:** `@types/node` 22 → 26, pyright 1.1.407 → 1.1.414,
  pytest >= 9, pytest-asyncio >= 1.4.

## 1.0.1

Fixed

- TypeScript: request fields that are optional in the contract and have a
  default may be omitted again, e.g. `agent_access` in
  `memoryStores.create`, `ttl_seconds` / `expires_with_session` (and the
  provider's `api_variant` / `endpoint_path`) in `agents.modelOverride.set`,
  `runtime_protection_enabled` in `orgs.machinePools.create`,
  `supports_tools` / `supports_reasoning` in
  `orgs.modelProviders.models.create`, `enabled` in `cronTriggers.create`,
  `page` in `integrations.inspectGitHubInstallations` and `read_only` in
  `machines.desktopSessions.create`. The server applies the default. Response types
  are unchanged: a field with a default is still always present. Python and
  Go already treated these fields as optional; their code is unchanged and
  they are released at 1.0.1 to keep one version across the three SDKs.

## 1.0.0

Breaking (ADR 0012): resource-style clients in all three languages, released
together as 1.0.0. Upgrade guide: [MIGRATION.md](MIGRATION.md).

- All languages: event streams reconnect like EventSource (dropped
  connection, server-ended response, `service_unavailable`), discard an
  unterminated frame and never end on their own; the custom tool runner has
  its own reconnect budget (unlimited by default), treats a 409 on submit as
  handled and never stops silently; every `{data, next_<param>}` list
  paginates; binary downloads are named `download` (verified artifacts:
  `downloadVerified`); token and base URL default to `BMA_TOKEN` /
  `BMA_BASE_URL`; uploads are not cut off by the default timeout and `0` /
  `None` disables it; a body that cannot be replayed is never retried.
- All languages: `BMA_BASE_URL` / `baseUrl` / `base_url` /
  `option.WithBaseURL` is the deployment **origin**
  (`https://api.staging.bma.beeos.ai`), like `ANTHROPIC_BASE_URL`; the native
  client adds `/api/v1`, the facade extensions `/v1`. A value that already
  ends with `/api/v1` (the 0.x API-root form) is accepted once, not doubled.
  `DEFAULT_BASE_URL` / `DefaultBaseURL` is now `https://api.bma.beeos.ai`
  (was `https://api.bma.beeos.ai/v1`).
- Go: generated names use Go initialisms (`ID`, `AgentID`, `IDs`, `URL`, ...).
- `tools/sdkgen` rejects flattened-params name collisions and HTTP methods
  the SDKs do not send; `tools/check_versions.sh` keeps one version across
  manifests, User-Agent constants and the release tag.

- TypeScript: resource-style client generated from
  `contracts/bma/sdk.resources.yaml` (230 methods; 14 daemon/WebSocket
  operations stay on the `bma.rest` escape hatch). Client `orgId` /
  `projectId` defaults, retries with generated idempotency keys, 60 s
  timeouts, `PagePromise` cursor lists, a discriminated event stream that
  reconnects on `service_unavailable`, status-named error classes with a typed
  `code`, `defineTool` and `agents.toolCalls.runner` for custom tools, and
  resource methods for the facade extensions.
- Python: `Bma` / `AsyncBma` with resource methods taking keyword arguments,
  pydantic v2 response models and TypedDict request types (`bma_sdk.types`)
  generated by `tools/sdkgen` (replaces openapi-python-client, attrs and
  `bma_sdk.rest`); same retries, pagination (`SyncCursorPage`,
  `AsyncPaginator`), typed event stream, error classes, `define_tool` +
  `agents.tool_calls.runner` and facade extension resources as TypeScript.
  New dependency `pydantic>=2.7`.
- Go: package `bma` at the module root (`bma.NewClient` + `option`
  package) with services such as `client.Agents.Sessions.New`, flat
  `<Resource><Method>Params`, `List` + `ListAutoPaging`, `Stream` with
  `AsAny()`, `AsAny()` on discriminated unions, `*bma.Error` with
  `bma.ErrorCode`, `DefineTool` + `Agents.ToolCalls.Runner`; facade extensions
  in package `facade`. Packages `rest` and `facadeext` are removed.
- `tools/sdkgen`: the generator fails when a contract operation is missing
  from the resource map.
- Docs: the READMEs require an explicit base URL while the hosted BMA service
  is in early access (the default origin `https://api.bma.beeos.ai` does not
  resolve yet; set `BMA_BASE_URL`, for example to the staging origin).

## bma-sdk v0.4.2

Repository migration; the Go import path changed. The code is identical to
bma-sdk 0.4.1.

- The SDK moved from `beeos-ai/bma-sdks` (archived) to
  [`beeos-ai/bma-sdk`](https://github.com/beeos-ai/bma-sdk), with its git
  history.
- **Go import path:** `github.com/beeos-ai/bma-sdks/go/...` →
  `github.com/beeos-ai/bma-sdk/...` (`github.com/beeos-ai/bma-sdk/rest`,
  `github.com/beeos-ai/bma-sdk/facadeext`; the module is now at the repository
  root). Update the imports and run `go get github.com/beeos-ai/bma-sdk@v0.4.2`.
  The old module is marked deprecated.
- npm `@beeos-ai/bma-sdk` and PyPI `bma-sdk` keep their names. TypeScript is
  in `typescript/`, Python in `python/`.
- One tag `v0.4.2` now releases all three languages (was `go/v*`, `ts/v*`,
  `python/v*`).

## bma-sdk v0.4.1

Tags `go/v0.4.1`, `ts/v0.4.1`, `python/v0.4.1` (`github.com/beeos-ai/bma-sdks/go`,
`@beeos-ai/bma-sdk@0.4.1`, PyPI `bma-sdk` 0.4.1). Contract refreshed to
beeos-ai/beeos-managed-agents@db2403f9.

### Breaking changes (Go)

- **Go nullable fields are now pointers (callers must dereference).** A
  nullable `$ref` (`anyOf`/`oneOf` with `null`) was generated as a plain value
  because OpenAPI 3.0 ignores keywords beside `$ref`, so `null` decoded to the
  zero value and could not be told apart from a real one. `tools/downgrade_openapi.py`
  now wraps it as `allOf: [$ref]` + `nullable: true`. For example
  `File.Scope` is `*FileScope`, `AgentMachine.MachinePoolId` and
  `Machine.MachinePoolId` are `*MachinePoolID`, and the nullable `Timestamp`
  fields (`CronTrigger.LastFiredAt`, `PersonalAccessToken.RevokedAt`, ...) are
  `*Timestamp`. Required nullable fields marshal `null` when nil. Optional
  nullable fields keep `omitempty`. TypeScript and Python already modelled null.

### Features

- Contract: agent executor binding (`GetAgentExecutorBinding`,
  `PutAgentExecutorBinding`) and MCP transport schemas, in all three SDKs.

## v0.4.0

| Family | Released | Tags | GitHub Releases |
| --- | --- | --- | --- |
| bma-executor-sdk 0.4.0 | 2026-10-31 (UTC) | `executor/v0.4.0`, `executor-ts/v0.4.0`, `executor-python/v0.4.0` | [Go](https://github.com/beeos-ai/bma-sdks/releases/tag/executor%2Fv0.4.0) · [TypeScript](https://github.com/beeos-ai/bma-sdks/releases/tag/executor-ts%2Fv0.4.0) · [Python](https://github.com/beeos-ai/bma-sdks/releases/tag/executor-python%2Fv0.4.0) |
| bma-sdk 0.4.0 | 2026-10-31 (UTC) | `go/v0.4.0`, `ts/v0.4.0`, `python/v0.4.0` | [Go](https://github.com/beeos-ai/bma-sdks/releases/tag/go%2Fv0.4.0) · [TypeScript](https://github.com/beeos-ai/bma-sdks/releases/tag/ts%2Fv0.4.0) · [Python](https://github.com/beeos-ai/bma-sdks/releases/tag/python%2Fv0.4.0) |

bma-executor-sdk 0.4.0 was released first (Go tag `executor/v0.4.0`, npm
`@beeos-ai/bma-executor-sdk@0.4.0`, PyPI `bma-executor-sdk` via
`executor-python/v0.4.0`). bma-sdk 0.4.0 (`go/v0.4.0`, `ts/v0.4.0`,
`python/v0.4.0`) follows with the REST snapshot regenerated from BMA main
(beeos-ai/beeos-managed-agents@ceee7dcf).

Two SDK families now ship from this repository, generated from the same BMA
contract and versioned independently:

| Family | Go | npm | PyPI |
| --- | --- | --- | --- |
| bma-sdk (REST + façade extensions) | `github.com/beeos-ai/bma-sdks/go` (tag `go/v0.4.0`) | `@beeos-ai/bma-sdk@0.4.0` (tag `ts/v0.4.0`) | `bma-sdk` 0.4.0 (tag `python/v0.4.0`) |
| bma-executor-sdk (executor protocol) | `github.com/beeos-ai/bma-sdks/executor` (tag `executor/v0.4.0`) | `@beeos-ai/bma-executor-sdk@0.4.0` (tag `executor-ts/v0.4.0`) | `bma-executor-sdk` 0.4.0 (tag `executor-python/v0.4.0`) |

Executor contract: `bma.executor.v1.1` (contract 1.1.0), snapshot and types
generated by BMA `make contract-sdk`; `contracts/bma/executor/lock.json`
records the BMA commit (beeos-ai/beeos-managed-agents@69c05b65, #278).

### bma-sdk REST and façade (contract at BMA ceee7dcf)

Breaking:

- The machine-daemon runtime operations were removed upstream
  (`registerMachineDaemonRuntime`, `endMachineDaemonRuntime`,
  `sleepMachineDaemonRuntime`, `socketMachineDaemonRuntime`) together with the
  `DaemonRuntime*` and `Process*Reconciliation*` schemas.
- `AgentSession.status` is required: `idle`, `running`, `rescheduling` or
  `terminated` (Go `AgentSessionStatus*` constants).
- Python: the REST `File` schema is generated as `ProjectFile`
  (`bma_sdk.rest.models.ProjectFile`), so it no longer shadows the generator's
  `bma_sdk.rest.types.File` upload payload; `upload_file` previously crashed
  parsing its own response.

New REST operations:

- Files API: `uploadFile`, `listFiles`, `getFile`, `getFileContent`,
  `deleteFile`; session resources `addSessionResource`,
  `listSessionResources`, `deleteSessionResource`; artifacts
  `uploadSessionArtifact`, `listSessionArtifacts`,
  `getSessionArtifactContent`, `promoteSessionArtifact`.
- Agent machines: `createAgentPersistentMachine`, `listAgentMachines`,
  `deleteAgentMachine`; `resumeMachine`; backups `createMachineBackup`,
  `listMachineBackups`, `restoreMachineFromBackup`.
- `cancelAgentSession`.
- Machine-daemon: session files/outputs and machine backup archive/restore
  endpoints.

Façade extensions: `POST/GET /v1/sessions/{id}/resources` and
`DELETE /v1/sessions/{id}/resources/{resource_id}` (`AddSessionResource`,
`ListSessionResources`, `DeleteSessionResource`), session files download;
`/v1/files` is the standard Anthropic surface. README shows upload → mount
into a session → list outputs in all three languages.
