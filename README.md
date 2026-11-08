# bma-sdk

Go, TypeScript and Python clients for the BMA (BeeOS Managed Agents) API,
version 2.0 (ADR 0025). Each is **the official Anthropic SDK plus the BMA
extensions**: the resources BMA shares with Claude Managed Agents (agents,
environments, sessions, events, files, skills, vaults, memory stores, …) are the
official SDK's own services with their signatures, and the BMA extensions
(machines, machine pools and grants, desktop and terminal sessions and their
tickets, organization projects) are typed services next to them under
`client.beta`, generated from [`contracts/bma/v2`](contracts/bma/v2). Code
written for the official SDK keeps working when `new Anthropic(...)` becomes
`new BmaClient(...)`.

| Language | Module / package | Official core | Client |
| --- | --- | --- | --- |
| Go | [`github.com/beeos-ai/bma-sdk/v2`](v2) | `anthropic-sdk-go/v2` v2.7.0 | `bmasdk.NewClient(...)` |
| TypeScript | [`@beeos-ai/bma-sdk`](typescript) | `@anthropic-ai/sdk` 1.6.0 | `new BmaClient({ apiKey, baseURL })` |
| Python | [`bma-sdk`](python) | `anthropic` 2.6.0 | `Bma(...)` / `AsyncBma(...)` |

The SDKs are for **servers** only (ADR 0025 B1): the API key is a tenant
credential. End users get single-use desktop or terminal tickets instead.

> The Executor Protocol SDK (executor, harness and agent ends) is
> [`beeos-ai/bma-executor-sdk`](https://github.com/beeos-ai/bma-executor-sdk).

## Quick start

All three read `BMA_API_KEY`, `BMA_BASE_URL` (the origin, e.g.
`https://api.staging.bma.beeos.ai`; default `https://api.bma.beeos.ai`) and
`BMA_PROJECT_ID` (header `x-bma-project-id`, needed when the key can see more
than one project). They never read the `ANTHROPIC_*` variables or the official
credential profiles, so an Anthropic key is never sent to BMA.

TypeScript (`npm install @beeos-ai/bma-sdk`; Node.js 20+, ESM):

```ts
import { BmaClient } from "@beeos-ai/bma-sdk";

const client = new BmaClient({ apiKey: process.env.BMA_API_KEY, baseURL: process.env.BMA_BASE_URL });

const session = await client.beta.sessions.create({ agent: agentId, environment_id: environmentId });

// Open the stream first, then send. A dropped stream resumes with Last-Event-ID.
const stream = await client.beta.sessions.events.stream(session.id);
await client.beta.sessions.events.send(session.id, {
  events: [{ type: "user.message", content: [{ type: "text", text: "Start the task." }] }],
});
for await (const event of stream) {
  if (event.type === "agent.message") console.log(event.content);
  else if (event.type === "session.status_idle") break;
}

// BMA extensions, same client
const machines = client.beta.machines.list({ limit: 20 }); // auto-paging
const ticket = await client.beta.terminalSessions.tickets.create(terminalId, {});
```

Python (`pip install bma-sdk`; Python 3.10+):

```python
from bma_sdk import Bma

client = Bma()  # BMA_API_KEY, BMA_BASE_URL, BMA_PROJECT_ID

session = client.beta.sessions.create(agent=agent_id, environment_id=environment_id)

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "Start the task."}]}],
    )
    for event in stream:
        if event.type == "agent.message":
            print(event.content)
        elif event.type == "session.status_idle":
            break

for machine in client.beta.machines.list(limit=20):  # auto-paging
    print(machine.id)
ticket = client.beta.terminal_sessions.tickets.create(terminal_id)
```

Go (`go get github.com/beeos-ai/bma-sdk/v2`; Go 1.25+):

```go
client := bmasdk.NewClient() // BMA_API_KEY, BMA_BASE_URL, BMA_PROJECT_ID
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{ /* … */ })
pager := client.Beta.Machines.ListAutoPaging(ctx, bmasdk.MachineListParams{})
```

See [`v2/README.md`](v2/README.md), [`typescript/README.md`](typescript/README.md)
and [`python/README.md`](python/README.md) for each language.

## `bma_*` fields, streams, idempotency

| | Go | TypeScript | Python |
| --- | --- | --- | --- |
| Read `bma_model_override`, `bma_harness` (session, agent), `bma_desktop`, `bma_machine` (environment), `bma_sequence`, `bma_input_id`, `bma_error_code` (events) | `SessionExtensions(s)`, `AgentExtensions`, `EnvironmentExtensions`, `EventExtensions` | `sessionExtensions(s)`, `agentExtensions`, `environmentExtensions`, `eventExtensions` | `session_extensions(s)`, `agent_extensions`, `environment_extensions`, `event_extensions` |
| Write them on the official create / update | request options `WithSessionModelOverride(…)`, `WithSessionModelOverridePatch`, `WithSessionModelOverrideRevoke()`, `WithHarness`, `WithEnvironmentDesktop` | typed fields of the official params: `bma_model_override`, `bma_harness`, `bma_desktop` (`null` revokes the override) | `**session_options(model_override=…, harness=…)`, `**agent_options(harness=…)`, `**environment_options(desktop=…)` (typed `extra_body`) |
| BMA's error reason (`error.code`) | `ErrorCode(err)` | `errorCode(err)` | `error_code(err)` |
| Project scope | `bmasdk.WithProject(id)` | `{ project }` option | `project=` argument |
| Idempotency key | `bmasdk.WithIdempotencyKey(k)` | header `Idempotency-Key` in the call's `headers` | `idempotency_key=` argument (extension creates only) |

- **Event stream resumption.** `sessions.events.stream` has the official
  signature and frames. When the connection drops or the server ends the
  stream, it reconnects with `Last-Event-ID` and returns every event once. One
  durable BMA event (one `bma_sequence`) projects into several frames that share
  the sequence and the server resumes after a whole sequence, so the client
  resumes after the *previous* sequence and skips the frames it already
  returned (by event id). Up to 5 failed attempts in a row, backoff 0.5–8 s; an
  API error other than 408/409/429/5xx, or closing/aborting the stream, ends it.
  The official, non-resuming stream stays reachable (Go
  `Events.BetaSessionEventService.StreamEvents`, TypeScript
  `Events.prototype.stream.call(client.beta.sessions.events, …)`, Python
  `Events.stream(client.beta.sessions.events, …)`).
- **Idempotency.** Extension creates (`machines.create`, `terminalSessions.create`,
  tickets, …) send a random `Idempotency-Key` once per call, so the official
  client's automatic retries resend the same key. CMA methods are never given
  a key automatically; pass one yourself to make a create safe to retry.
- **Errors** are the official error classes (`*anthropic.Error`,
  `APIError` / `NotFoundError`…, `anthropic.APIStatusError`…).
- Known server gap (staging, 2026-11-08): a stream resumed with
  `Last-Event-ID` replays the durable events but not the `session.status_*`
  events the list derives for them (ids `sesst_…`, e.g. the
  `session.status_idle` of `requires_action`). Do not rely on that idle after a
  reconnect.

## Signatures against the official SDKs

Shared resources are the official services unchanged; the extensions follow the
official naming of each language.

| Resource | Official Go (`anthropic-sdk-go/v2`) | Official TypeScript (`@anthropic-ai/sdk`) | Official Python (`anthropic`) | bma-sdk 2.0 |
| --- | --- | --- | --- | --- |
| Create | `Beta.Agents.New(ctx, params, opts…)` | `beta.agents.create(params, options?)` | `beta.agents.create(*, name=…, model=…)` | identical (Agents, Environments, Sessions, Files, Skills, Vaults, MemoryStores, UserProfiles, Models, …) |
| Get | `Beta.Agents.Get(ctx, id, params, opts…)` | `beta.agents.retrieve(id, params?, options?)` | `beta.agents.retrieve(id)` | identical |
| List | `Beta.Agents.List` / `ListAutoPaging` | `beta.agents.list()` (async iterable) | `beta.agents.list()` (iterable) | identical |
| Stream events | `Beta.Sessions.Events.StreamEvents(ctx, id, params, opts…) *ssestream.Stream[…]` | `beta.sessions.events.stream(id, params?, options?)` | `beta.sessions.events.stream(id, …)` | same signature, resumes |
| Extension create | — | — | — | Go `Beta.Machines.New(ctx, MachineNewParams)`; TS `beta.machines.create(params)`; Python `beta.machines.create(*, …)` |
| Extension get | — | — | — | Go `Beta.Machines.Get(ctx, id)`; TS `beta.machines.retrieve(id)`; Python `beta.machines.retrieve(id)` |
| Extension action | — | — | — | Go `Beta.DesktopSessions.AcquireControl(ctx, id, params)`; TS `beta.desktopSessions.acquireControl(id, params)`; Python `beta.desktop_sessions.acquire_control(id, *, …)` |
| Nested | — | — | — | Go `Beta.MachinePools.Grants.New(ctx, poolID, …)`; TS `beta.machinePools.grants.create(poolID, params)`; Python `beta.machine_pools.grants.create(pool_id, *, …)` |

Extensions (all three languages; names in each language's case, e.g.
`desktop_sessions.acquire_control`):

| Resource | Methods |
| --- | --- |
| `beta.organization.projects` | `create(organizationID, …)`, `list(organizationID, …)` |
| `beta.machines` | `create`, `retrieve`, `update`, `list`, `delete`, `resume`, `getCapabilities` |
| `beta.machinePools` | `create`, `retrieve`, `update`, `list`, `delete`, `checkConnection` |
| `beta.machinePools.grants` | `create`, `retrieve`, `update`, `list`, `delete` |
| `beta.desktopSessions` | `create`, `retrieve`, `close`, `acquireControl`, `renewControl`, `releaseControl`, `handbackControl`, `sendActions`, `screenshot`, `resumeAgent`, `confirmAction` |
| `beta.desktopSessions.tickets` | `create` (purpose `watch`) |
| `beta.terminalSessions` | `create`, `retrieve`, `list`, `close` |
| `beta.terminalSessions.tickets` | `create` (purpose `connect`) |

Go names the get method `Get`; TypeScript and Python name it `retrieve`, as
their official SDKs do. Path parameters are positional; the request body fields
are keyword arguments in Python and one params object in TypeScript and Go.
Not in 2.0: the deprecated extension routes (`/orgs/{org_id}/projects`,
`watch_tickets`, `connection_tickets`) and the native `/api/v1` resources of
1.x; see [MIGRATION.md](MIGRATION.md).

Limitation: the official `with_raw_response` / `with_streaming_response`
wrappers of Python cover the official resources only; the BMA extensions return
parsed models. In every language the official credential features (profiles,
federation) are disabled: authentication is the BMA API key.

## Versions

2.0.0, one version for all three languages (Go module `…/v2`, npm, PyPI),
released from one tag `v2.0.0`. Until that tag, use a commit (Go pseudo-version
`github.com/beeos-ai/bma-sdk/v2 v2.0.0-<time>-<sha>`) or the built packages.

| Compatibility | bma-sdk 2.0.0 |
| --- | --- |
| BMA contract | extensions at BMA commit `32a146ec4` ([`contracts/bma/v2/lock.json`](contracts/bma/v2/lock.json)) |
| Protocol | Anthropic-style `/v1` |
| Official cores | anthropic-sdk-go/v2 v2.7.0, @anthropic-ai/sdk 1.6.0, anthropic 2.6.0 (exact pins; an upgrade is a PR with the staging tests) |
| Runtimes | Go 1.25+ (2.0 module; the official v2 requires it), Node.js 20+ (ESM), Python 3.10+ |

1.x (Go root module, npm and PyPI 1.0.1) is frozen at tag `v1.0.1`; the 1.x
README and sources are at that tag. Release notes: [CHANGELOG](CHANGELOG.md).

## Development

```bash
./tools/generate.sh                                  # regenerate Go, TypeScript and Python
uv run --no-project --with pyyaml --with jsonschema \
  python tools/check_contract.py [--source ../beeos-managed-agents]
(cd v2 && go vet ./... && go test -race ./...)
(cd typescript && npm ci && npm run build && npm test)
(cd python && uv run pytest -q && uv run pyright)
```

`tools/generate.sh` needs Python 3 with PyYAML, Go 1.25+, Node 20+ and uv; it
pins oapi-codegen v2.7.0 (Go models), openapi-typescript 7.13.0 (TypeScript
types) and ruff (formatting of the Python output). The extension services come
from the contract plus [`contracts/bma/v2/sdk.resources.yaml`](contracts/bma/v2/sdk.resources.yaml)
through [`tools/sdkgen`](tools/sdkgen) (`go2gen.py`, `ts2gen.py`, `py2gen.py`);
an unmapped operation fails the generation. Never edit generated files by
hand. Refresh the contract with
`python3 tools/v2/bundle_contract.py --source <beeos-managed-agents checkout>`.

Live tests against staging (they create and remove an environment, an agent and
a session, and refuse to run against `api.bma.beeos.ai`; set
`BMA_API_KEY`, `BMA_BASE_URL`, `BMA_PROJECT_ID`, `BMA_ORG_ID`, and
`no_proxy='*'` behind a proxy):

```bash
(cd v2 && BMA_INTEGRATION=1 go test -run TestStaging -v -timeout 20m ./...)
(cd typescript && BMA_INTEGRATION=1 npm test)
(cd python && BMA_INTEGRATION=1 uv run pytest tests/test_staging.py -s)
```

## Release

One tag `v<version>` releases all three languages at the same version: it must
be on `main`, and [`tools/check_versions.sh`](tools/check_versions.sh) checks it
against `typescript/package.json`, `python/pyproject.toml` (the Python client
reads its version from the installed metadata) and the constants
`typescript/src/version.ts` and `v2/client.go` (CI runs the same check without a
tag). [`release.yaml`](.github/workflows/release.yaml) first runs
[`ci.yaml`](.github/workflows/ci.yaml) (regenerate every SDK with no diff,
contract drift check, Go, TypeScript and Python tests), then publishes.

| Channel | Publishes | Credentials |
| --- | --- | --- |
| Go | nothing; the module `…/v2` comes from the tag (directory `v2/`) | none |
| npm | `@beeos-ai/bma-sdk` with provenance | secret `NPM_TOKEN` in the `releases` environment |
| PyPI | `bma-sdk` | a PyPI Trusted Publisher on `bma-sdk`: owner `beeos-ai`, repository `bma-sdk`, workflow `release.yaml`, environment `releases` |

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
