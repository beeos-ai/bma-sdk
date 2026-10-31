# bma-sdk

Python client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml), plus
the BMA extensions to the Anthropic Managed Agents API.

```python
from bma_sdk import BmaClient, unwrap
from bma_sdk.rest.api.agents import create_agent_input, create_agent_session
from bma_sdk.rest.models import CreateAgentInputRequest, CreateAgentSessionRequest, TextContentBlock

with BmaClient(token, "https://host/api/v1") as bma:
    session = unwrap(create_agent_session.sync_detailed(
        org, project, agent, client=bma.rest,
        body=CreateAgentSessionRequest(idempotency_key="task-1"),
    )).session
    unwrap(create_agent_input.sync_detailed(
        org, project, agent, client=bma.rest, session_id=session.id,
        body=CreateAgentInputRequest(content_blocks=[TextContentBlock(type_="text", text="Start.")]),
    ))
    for frame in bma.stream_events(org, project, agent, session_id=session.id):
        print(frame.event, frame.sequence)
```

`bma_sdk.rest` contains one module per contract operation with
`sync`/`sync_detailed`/`asyncio`/`asyncio_detailed` functions. `BmaClient`
adds bearer authentication, `stream_events`, and `download_artifact` (size and
sha256 verified).

## BMA extensions to the Anthropic facade

Use the official Anthropic SDK for `/v1/agents`, `/v1/environments`,
`/v1/sessions` and events. The routes BMA adds:

```python
from bma_sdk.facade_extensions import FacadeExtensionsClient, bma_sequence

with FacadeExtensionsClient(api_key, "https://host", project_id="proj_...") as ext:
    ticket = ext.get_session_desktop_stream(session_id, desktop_session_id=desktop_id)
    ext.upload_session_file(session_id, "report.pdf", data)
    page = ext.list_session_files(session_id, limit=100)
```

The module also exports `ModelConfigOverride`, `MCPServerBMAAuth`,
`IDEMPOTENCY_KEY_HEADER`, and `bma_sequence(event)`.
