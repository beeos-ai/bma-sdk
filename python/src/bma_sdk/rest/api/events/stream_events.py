from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_input_event import AgentInputEvent
from ...models.context_checkpoint_event import ContextCheckpointEvent
from ...models.error import Error
from ...models.executor_event import ExecutorEvent
from ...models.model_output_delta import ModelOutputDelta
from ...models.model_output_event import ModelOutputEvent
from ...models.stream_events_response_4xx import StreamEventsResponse4XX
from ...models.stream_events_response_5xx import StreamEventsResponse5XX
from ...models.tool_call_update import ToolCallUpdate
from ...models.tool_result_event import ToolResultEvent
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    session_id: Union[Unset, str] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    stream_deltas: Union[Unset, bool] = UNSET,
    last_event_id: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = str(last_event_id)

    params: dict[str, Any] = {}

    params["session_id"] = session_id

    params["after_sequence"] = after_sequence

    params["stream_deltas"] = stream_deltas

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/events/stream".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_0 = AgentInputEvent.from_dict(data)

                return componentsschemas_agent_event_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_1 = ModelOutputEvent.from_dict(data)

                return componentsschemas_agent_event_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_2 = ToolResultEvent.from_dict(data)

                return componentsschemas_agent_event_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_3 = ContextCheckpointEvent.from_dict(
                    data
                )

                return componentsschemas_agent_event_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_4 = ExecutorEvent.from_dict(data)

                return componentsschemas_agent_event_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_stream_data_type_1 = (
                    ToolCallUpdate.from_dict(data)
                )

                return componentsschemas_agent_event_stream_data_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_stream_data_type_2 = (
                    ModelOutputDelta.from_dict(data)
                )

                return componentsschemas_agent_event_stream_data_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_agent_event_stream_data_type_3 = Error.from_dict(data)

            return componentsschemas_agent_event_stream_data_type_3

        response_200 = _parse_response_200(response.text)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = StreamEventsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = StreamEventsResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    stream_deltas: Union[Unset, bool] = UNSET,
    last_event_id: Union[Unset, int] = UNSET,
) -> Response[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    """Stream events

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        after_sequence (Union[Unset, int]):
        stream_deltas (Union[Unset, bool]):
        last_event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, StreamEventsResponse4XX, StreamEventsResponse5XX, Union['AgentInputEvent', 'ContextCheckpointEvent', 'Error', 'ExecutorEvent', 'ModelOutputDelta', 'ModelOutputEvent', 'ToolCallUpdate', 'ToolResultEvent']]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        after_sequence=after_sequence,
        stream_deltas=stream_deltas,
        last_event_id=last_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    stream_deltas: Union[Unset, bool] = UNSET,
    last_event_id: Union[Unset, int] = UNSET,
) -> Optional[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    """Stream events

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        after_sequence (Union[Unset, int]):
        stream_deltas (Union[Unset, bool]):
        last_event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, StreamEventsResponse4XX, StreamEventsResponse5XX, Union['AgentInputEvent', 'ContextCheckpointEvent', 'Error', 'ExecutorEvent', 'ModelOutputDelta', 'ModelOutputEvent', 'ToolCallUpdate', 'ToolResultEvent']]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        session_id=session_id,
        after_sequence=after_sequence,
        stream_deltas=stream_deltas,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    stream_deltas: Union[Unset, bool] = UNSET,
    last_event_id: Union[Unset, int] = UNSET,
) -> Response[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    """Stream events

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        after_sequence (Union[Unset, int]):
        stream_deltas (Union[Unset, bool]):
        last_event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, StreamEventsResponse4XX, StreamEventsResponse5XX, Union['AgentInputEvent', 'ContextCheckpointEvent', 'Error', 'ExecutorEvent', 'ModelOutputDelta', 'ModelOutputEvent', 'ToolCallUpdate', 'ToolResultEvent']]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        after_sequence=after_sequence,
        stream_deltas=stream_deltas,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    stream_deltas: Union[Unset, bool] = UNSET,
    last_event_id: Union[Unset, int] = UNSET,
) -> Optional[
    Union[
        Error,
        StreamEventsResponse4XX,
        StreamEventsResponse5XX,
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "Error",
            "ExecutorEvent",
            "ModelOutputDelta",
            "ModelOutputEvent",
            "ToolCallUpdate",
            "ToolResultEvent",
        ],
    ]
]:
    """Stream events

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        after_sequence (Union[Unset, int]):
        stream_deltas (Union[Unset, bool]):
        last_event_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, StreamEventsResponse4XX, StreamEventsResponse5XX, Union['AgentInputEvent', 'ContextCheckpointEvent', 'Error', 'ExecutorEvent', 'ModelOutputDelta', 'ModelOutputEvent', 'ToolCallUpdate', 'ToolResultEvent']]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            session_id=session_id,
            after_sequence=after_sequence,
            stream_deltas=stream_deltas,
            last_event_id=last_event_id,
        )
    ).parsed
