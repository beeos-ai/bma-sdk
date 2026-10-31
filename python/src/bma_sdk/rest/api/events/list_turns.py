from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_agent_turns_response import ListAgentTurnsResponse
from ...models.list_turns_response_4xx import ListTurnsResponse4XX
from ...models.list_turns_response_5xx import ListTurnsResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    session_id: Union[Unset, str] = UNSET,
    before_turn_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["session_id"] = session_id

    params["before_turn_sequence"] = before_turn_sequence

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/turns".format(
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
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
]:
    if response.status_code == 200:
        response_200 = ListAgentTurnsResponse.from_dict(response.json())

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
        response_4xx = ListTurnsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListTurnsResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
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
    before_turn_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
]:
    """List turns

     Returns turns newest first. Use the returned next_before_turn_sequence as before_turn_sequence to
    fetch older turns.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_turn_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        before_turn_sequence=before_turn_sequence,
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
    before_turn_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
]:
    """List turns

     Returns turns newest first. Use the returned next_before_turn_sequence as before_turn_sequence to
    fetch older turns.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_turn_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        session_id=session_id,
        before_turn_sequence=before_turn_sequence,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: Union[Unset, str] = UNSET,
    before_turn_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
]:
    """List turns

     Returns turns newest first. Use the returned next_before_turn_sequence as before_turn_sequence to
    fetch older turns.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_turn_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        before_turn_sequence=before_turn_sequence,
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
    before_turn_sequence: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[
    Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
]:
    """List turns

     Returns turns newest first. Use the returned next_before_turn_sequence as before_turn_sequence to
    fetch older turns.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        before_turn_sequence (Union[Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentTurnsResponse, ListTurnsResponse4XX, ListTurnsResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            session_id=session_id,
            before_turn_sequence=before_turn_sequence,
            limit=limit,
        )
    ).parsed
