# bma-sdk

[![PyPI](https://img.shields.io/pypi/v/bma-sdk.svg)](https://pypi.org/project/bma-sdk/)

Python client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml), plus
the BMA extensions to the Anthropic Managed Agents API.

| | |
| --- | --- |
| Version | see [CHANGELOG](../CHANGELOG.md) |
| Contract | BMA REST snapshot recorded in [`contracts/bma/lock.json`](../contracts/bma/lock.json) |
| Python | 3.10 or newer; depends on httpx and pydantic 2 |

```sh
pip install bma-sdk
```

```python
from bma_sdk import Bma

# token, base_url, org_id and project_id default to BMA_TOKEN, BMA_BASE_URL,
# BMA_ORG_ID and BMA_PROJECT_ID
bma = Bma()
created = bma.agents.sessions.create(agent_id, idempotency_key="task-1")
bma.agents.inputs.create(
    agent_id,
    session_id=created.session.id,
    content_blocks=[{"type": "text", "text": "Start the task."}],
)
for ev in bma.agents.events.stream(agent_id, session_id=created.session.id, stream_deltas=True):
    if ev.event == "model_output":          # narrows ev.data to ModelOutputEvent
        print(ev.sequence, ev.data.content_blocks)
    elif ev.event == "tool_call_update":
        print(ev.data.tool_call_id, ev.data.state)
```

Pass `base_url` (or set `BMA_BASE_URL`) for your deployment, the API root
including `/api/v1`; the default `https://api.bma.beeos.ai/v1` is not live
yet. `org_id` / `project_id` default to `BMA_ORG_ID` / `BMA_PROJECT_ID`; every
method accepts `org_id=` / `project_id=` to override them. `AsyncBma` has the same resources with
`async` methods.

- **Methods** follow [`contracts/bma/sdk.resources.yaml`](../contracts/bma/sdk.resources.yaml):
  path IDs are positional, query, header and body fields are keyword
  arguments with their wire names. Omitted arguments are not sent; `None`
  sends JSON `null`.
- **Types**: responses are pydantic models and request objects are
  TypedDicts (`TextContentBlockParam` ...), all in `bma_sdk.types`. Responses
  are built without validation, so fields a newer server adds are kept.
- **Pagination**: every list whose response is `{data, next_<param>}`
  (`cursor`, `page`, `before_id`/`after_id`, `before_sequence`/`after_sequence`)
  returns a `SyncCursorPage` (`data`, `next_cursor` = the next value of that
  parameter); iterating it walks every page (`AsyncBma`: `await` for the
  first page, `async for` for all). `agents.events.list` pages forward, or
  backward when you pass `before_sequence`.
- **Event stream**: frames are discriminated by `event`. Like EventSource, the
  stream reconnects from the last durable frame (`Last-Event-ID`) when the
  connection drops, the server ends the response, or on a
  `service_unavailable` error frame, discarding a frame cut off at the end;
  it never ends on its own and raises once `max_retries` reconnects in a row
  received no data. Any other error frame raises `EventStreamError`.
- **Errors and retries**: `BmaApiError` subclasses by status
  (`NotFoundError`, `ConflictError`, `RateLimitError` ...) with `code`. Reads
  and calls that accept an `Idempotency-Key` retry 408/429/5xx and connection
  errors with a generated key reused across attempts; other writes retry only
  429/503 and requests that never reached the server; 409 is never retried.
  Defaults: 2 retries, 60 s timeout (`Bma(max_retries=, timeout=)`,
  `bma.with_options(...)`, `timeout=` per call). The timeout is httpx's
  per-phase timeout (connect, write, read, pool), so long uploads and
  downloads are not cut off; pass an `httpx.Timeout` to set the phases or
  `None` for no timeout. A file object `body` is rewound for a retry when it
  is seekable; an unseekable stream is sent once and never retried.
- **Downloads**: `files.download`, `agents.artifacts.download`, ... return the
  `httpx.Response`; `bma.agents.artifacts.download_verified(artifact,
  max_bytes=...)` verifies size and sha256.

## Custom tools

```python
from pydantic import BaseModel
from bma_sdk import ToolContext, ToolError, define_tool

class Weather(BaseModel):
    city: str

def get_weather(input: Weather, ctx: ToolContext) -> str:
    return f"Sunny in {input.city}"

weather = define_tool(name="get_weather", description="Current weather", input_model=Weather, run=get_weather)
# weather.definition goes into the agent config under tools.get_weather
bma.agents.tool_calls.runner(agent_id, session_id=session_id, tools=[weather]).until_done()
```

Raise `ToolError(text)` to report a failed call to the model. With
`AsyncBma`, tools may be `async` and run concurrently. The runner reconnects
its event stream without limit by default (`max_reconnects=` bounds it),
treats a 409 on submit (another consumer answered) as handled, and
`until_done()` raises the error that stopped it; it returns only after
`stop()`.

## BMA extensions to the Anthropic facade

Use the official Anthropic SDK for `/v1/agents`, `/v1/environments`,
`/v1/sessions` and events. The routes BMA adds:

```python
from bma_sdk.facade_extensions import FacadeExtensions, bma_sequence

with FacadeExtensions(api_key=api_key, base_url="https://host", project_id="proj_...") as ext:
    ticket = ext.sessions.desktop.stream(session_id, desktop_session_id=desktop_id)
    ext.sessions.files.upload(session_id, file=("report.pdf", data))
    page = ext.sessions.files.list(session_id, limit=100)
```

Models such as `ModelConfigOverride` and `MCPServerBMAAuth` are in
`bma_sdk.facade_extensions.types`; `bma_sequence(event)` reads the resume
cursor of an Anthropic SDK event.

The executor protocol (executor, harness and agent ends) is the separate
package [`bma-executor-sdk`](https://github.com/beeos-ai/bma-executor-sdk/tree/main/python).
