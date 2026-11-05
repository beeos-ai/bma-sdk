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
import os

from bma_sdk import Bma

bma = Bma(
    token=os.environ["BMA_API_KEY"],
    base_url=os.environ["BMA_BASE_URL"] + "/api/v1",
    org_id=os.environ["BMA_ORG_ID"],          # default scope of every method
    project_id=os.environ["BMA_PROJECT_ID"],
)
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

Pass `base_url` for your deployment (the API root including `/api/v1`); the
default `https://api.bma.beeos.ai/v1` is not live yet. `org_id` / `project_id`
default to `BMA_ORG_ID` / `BMA_PROJECT_ID`; every method accepts `org_id=` /
`project_id=` to override them. `AsyncBma` has the same resources with
`async` methods.

- **Methods** follow [`contracts/bma/sdk.resources.yaml`](../contracts/bma/sdk.resources.yaml):
  path IDs are positional, query, header and body fields are keyword
  arguments with their wire names. Omitted arguments are not sent; `None`
  sends JSON `null`.
- **Types**: responses are pydantic models and request objects are
  TypedDicts (`TextContentBlockParam` ...), all in `bma_sdk.types`. Responses
  are built without validation, so fields a newer server adds are kept.
- **Pagination**: cursor lists return a `SyncCursorPage`; iterating it walks
  every page (`AsyncBma`: `await` for the first page, `async for` for all).
- **Event stream**: frames are discriminated by `event`; a
  `service_unavailable` error frame or a dropped connection reconnects from
  the last durable frame (`Last-Event-ID`), any other error frame raises
  `EventStreamError`.
- **Errors and retries**: `BmaApiError` subclasses by status
  (`NotFoundError`, `ConflictError`, `RateLimitError` ...) with `code`. Reads
  and calls that accept an `Idempotency-Key` retry 408/429/5xx and connection
  errors with a generated key reused across attempts; other writes retry only
  429/503 and requests that never reached the server; 409 is never retried.
  Defaults: 2 retries, 60 s per attempt (`Bma(max_retries=, timeout=)`,
  `bma.with_options(...)`, `timeout=` per call).
- **Artifacts**: `bma.agents.artifacts.download(artifact, max_bytes=...)`
  verifies size and sha256.

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
`AsyncBma`, tools may be `async` and run concurrently.

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
