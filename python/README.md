# bma-sdk (Python)

[![PyPI](https://img.shields.io/pypi/v/bma-sdk.svg)](https://pypi.org/project/bma-sdk/)

Python client for BMA, version 2.0 (ADR 0025): **the official
[`anthropic`](https://pypi.org/project/anthropic/) 2.6.0 SDK plus the BMA
extensions**. `Bma` and `AsyncBma` subclass `anthropic.Anthropic` and
`anthropic.AsyncAnthropic`, so every Claude Managed Agents resource under
`client.beta` (agents, environments, sessions, events, files, skills, vaults,
memory stores, …) is the official one with its signatures; the BMA extensions
(`machines`, `machine_pools` and `.grants`, `desktop_sessions` and `.tickets`,
`terminal_sessions` and `.tickets`, `organization.projects`) are generated from
[`contracts/bma/v2/extensions.openapi.yaml`](../contracts/bma/v2/extensions.openapi.yaml)
and use the same client: base URL, authentication, retries, timeouts, httpx
client, middleware and exceptions. Server side only: the API key is a tenant
credential (hand end users a ticket, never the key).

| | |
| --- | --- |
| Version | 2.2.0, see [CHANGELOG](../CHANGELOG.md); from 1.x: [MIGRATION](../MIGRATION.md#python-1x--20) |
| Official core | `anthropic` 2.6.0 (exact pin) |
| Python | 3.10 or newer |

```python
import bma_sdk
from bma_sdk import Bma

# api_key: BMA_API_KEY, base_url: BMA_BASE_URL (default https://api.bma.beeos.ai),
# project: BMA_PROJECT_ID. ANTHROPIC_* is never read.
client = Bma()

session = client.beta.sessions.create(
    agent=agent_id,
    environment_id=environment_id,
    **bma_sdk.session_options(model_override={"model": "deepseek-flash"}),  # typed BMA field
)
print(bma_sdk.session_extensions(session).model_override)

# Open the stream first, then send. A dropped stream resumes with Last-Event-ID
# and returns every event once.
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "Start the task."}]}],
    )
    for event in stream:
        if event.type == "session.status_idle":
            break

# Extensions
for machine in client.beta.machines.list(limit=20):
    print(machine.id)
term = client.beta.terminal_sessions.create(machine_id=machine_id)  # sends an Idempotency-Key
ticket = client.beta.terminal_sessions.tickets.create(term.id)  # single use; give it to the end user

try:
    client.beta.machines.retrieve("mch_x")
except bma_sdk.NotFoundError as err:
    print(bma_sdk.error_code(err))  # BMA's error.code, e.g. "machine_not_found"
```

`AsyncBma` is the same with `await` / `async for` (`await client.beta.sessions.events.stream(id)`).

To send first, use `send_and_stream`: it opens the stream at the cursor read
before the send (`bma_resume_cursor`), so frames an executor wrote before the
stream opened are not lost. `replayed` is true when the server gave no cursor
and the stream starts at `Last-Event-ID: 0` (pick your turn by `bma_input_id`).

```python
result = client.beta.sessions.events.send_and_stream(session.id, events=[
    {"type": "user.message", "content": [{"type": "text", "text": "Next step."}]},
])
with result.stream as stream:
    for event in stream:
        if event.type == "session.status_idle":
            break
```
(`await client.beta.sessions.events.send_and_stream(...)` on `AsyncBma`.)

- **Extension fields.** `session_extensions`, `agent_extensions`,
  `environment_extensions` and `event_extensions` read `bma_*` response fields
  as typed values. To write them on the official create / update, splat the
  typed `extra_body` of `session_options(model_override=…, harness=…)`,
  `agent_options(harness=…)` or `environment_options(desktop=…)`
  (`model_override=None` revokes).
- **Project.** `Bma(project=…)` sets `bma-workspace-id`;
  `client.with_options(project=…)` copies the client into another project.
- **Idempotency.** Extension creates send a random `Idempotency-Key` once per
  call, so automatic retries resend it; pass `idempotency_key=` to choose it.
  CMA creates get none unless you pass one (`extra_headers={"Idempotency-Key": …}`).
- Not wrapped: the official `with_raw_response` / `with_streaming_response`
  cover the official resources only. Credential features of the official
  client (profiles, `auth_token`, federation) are disabled: authentication is
  the BMA API key.

## Development

```bash
uv run pytest -q    # unit tests against a local server; BMA_INTEGRATION=1 adds tests/test_staging.py
uv run pyright
```

`src/bma_sdk/_generated/` is written by `tools/generate.sh`
(`tools/sdkgen/py2gen.py`); never edit it by hand.
