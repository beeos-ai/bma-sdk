from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_agent_events_response import ListAgentEventsResponse
from ...models.list_events_response_4xx import ListEventsResponse4XX
from ...models.list_events_response_5xx import ListEventsResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    session_id: Union[Unset, str] = UNSET,
    before_sequence: Union[Unset, int] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["session_id"] = session_id

    params["before_sequence"] = before_sequence

    params["after_sequence"] = after_sequence

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/events".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
]:
    if response.status_code == 200:
        response_200 = ListAgentEventsResponse.from_dict(response.json())

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
        response_4xx = ListEventsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListEventsResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
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
    before_sequence: Union[Unset, int] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
) -> Response[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
]:
    """List events

     Returns one page of agent events, chronological within the page. Forward pagination (after_sequence)
    walks from a known boundary toward the present using next_after_sequence. Backward pagination
    (before_sequence) starts at the latest events and walks toward the beginning using
    next_before_sequence; passing before_sequence takes precedence over after_sequence.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_sequence (Union[Unset, int]):
        after_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        before_sequence=before_sequence,
        after_sequence=after_sequence,
        limit=limit,
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
    before_sequence: Union[Unset, int] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
) -> Optional[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
]:
    """List events

     Returns one page of agent events, chronological within the page. Forward pagination (after_sequence)
    walks from a known boundary toward the present using next_after_sequence. Backward pagination
    (before_sequence) starts at the latest events and walks toward the beginning using
    next_before_sequence; passing before_sequence takes precedence over after_sequence.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_sequence (Union[Unset, int]):
        after_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        session_id=session_id,
        before_sequence=before_sequence,
        after_sequence=after_sequence,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    before_sequence: Union[Unset, int] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
) -> Response[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
]:
    """List events

     Returns one page of agent events, chronological within the page. Forward pagination (after_sequence)
    walks from a known boundary toward the present using next_after_sequence. Backward pagination
    (before_sequence) starts at the latest events and walks toward the beginning using
    next_before_sequence; passing before_sequence takes precedence over after_sequence.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_sequence (Union[Unset, int]):
        after_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        before_sequence=before_sequence,
        after_sequence=after_sequence,
        limit=limit,
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
    before_sequence: Union[Unset, int] = UNSET,
    after_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
) -> Optional[
    Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
]:
    """List events

     Returns one page of agent events, chronological within the page. Forward pagination (after_sequence)
    walks from a known boundary toward the present using next_after_sequence. Backward pagination
    (before_sequence) starts at the latest events and walks toward the beginning using
    next_before_sequence; passing before_sequence takes precedence over after_sequence.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_sequence (Union[Unset, int]):
        after_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentEventsResponse, ListEventsResponse4XX, ListEventsResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            session_id=session_id,
            before_sequence=before_sequence,
            after_sequence=after_sequence,
            limit=limit,
        )
    ).parsed
