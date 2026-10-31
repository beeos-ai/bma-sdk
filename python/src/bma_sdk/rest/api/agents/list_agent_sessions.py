from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_agent_sessions_response import ListAgentSessionsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    include_archived: Union[Unset, bool] = False,
    before_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["include_archived"] = include_archived

    params["before_id"] = before_id

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ListAgentSessionsResponse]]:
    if response.status_code == 200:
        response_200 = ListAgentSessionsResponse.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ListAgentSessionsResponse]]:
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
    include_archived: Union[Unset, bool] = False,
    before_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[Error, ListAgentSessionsResponse]]:
    """List agent sessions

     Lists the agent's conversation sessions, newest first. The default session is the legacy /api/v1
    target.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        include_archived (Union[Unset, bool]):  Default: False.
        before_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentSessionsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        include_archived=include_archived,
        before_id=before_id,
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
    include_archived: Union[Unset, bool] = False,
    before_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[Error, ListAgentSessionsResponse]]:
    """List agent sessions

     Lists the agent's conversation sessions, newest first. The default session is the legacy /api/v1
    target.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        include_archived (Union[Unset, bool]):  Default: False.
        before_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentSessionsResponse]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        include_archived=include_archived,
        before_id=before_id,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_archived: Union[Unset, bool] = False,
    before_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[Error, ListAgentSessionsResponse]]:
    """List agent sessions

     Lists the agent's conversation sessions, newest first. The default session is the legacy /api/v1
    target.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        include_archived (Union[Unset, bool]):  Default: False.
        before_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentSessionsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        include_archived=include_archived,
        before_id=before_id,
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
    include_archived: Union[Unset, bool] = False,
    before_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[Error, ListAgentSessionsResponse]]:
    """List agent sessions

     Lists the agent's conversation sessions, newest first. The default session is the legacy /api/v1
    target.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        include_archived (Union[Unset, bool]):  Default: False.
        before_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentSessionsResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            include_archived=include_archived,
            before_id=before_id,
            limit=limit,
        )
    ).parsed
