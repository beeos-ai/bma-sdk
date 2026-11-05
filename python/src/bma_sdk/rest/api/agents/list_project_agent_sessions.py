from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_project_agent_sessions_order import (
    ListProjectAgentSessionsOrder,
)
from ...models.list_project_agent_sessions_response import (
    ListProjectAgentSessionsResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    agent_profile_id: Union[Unset, str] = UNSET,
    include_archived: Union[Unset, bool] = False,
    include_default: Union[Unset, bool] = False,
    include_subagents: Union[Unset, bool] = False,
    order: Union[Unset, ListProjectAgentSessionsOrder] = "desc",
    after_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["agent_profile_id"] = agent_profile_id

    params["include_archived"] = include_archived

    params["include_default"] = include_default

    params["include_subagents"] = include_subagents

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order

    params["order"] = json_order

    params["after_id"] = after_id

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-sessions".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ListProjectAgentSessionsResponse]]:
    if response.status_code == 200:
        response_200 = ListProjectAgentSessionsResponse.from_dict(response.json())

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
) -> Response[Union[Error, ListProjectAgentSessionsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    agent_profile_id: Union[Unset, str] = UNSET,
    include_archived: Union[Unset, bool] = False,
    include_default: Union[Unset, bool] = False,
    include_subagents: Union[Unset, bool] = False,
    order: Union[Unset, ListProjectAgentSessionsOrder] = "desc",
    after_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[Error, ListProjectAgentSessionsResponse]]:
    """List the project's agent sessions

     Lists the conversation sessions of every agent in the project, ordered by creation time. Each
    agent's default session (the legacy /api/v1 conversation), archived sessions and subagent sessions
    are left out unless requested. Pages are keyset pages: pass the last session of a page as `after_id`
    with the same `order` to read the next one.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (Union[Unset, str]):
        include_archived (Union[Unset, bool]):  Default: False.
        include_default (Union[Unset, bool]):  Default: False.
        include_subagents (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ListProjectAgentSessionsOrder]):  Default: 'desc'.
        after_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListProjectAgentSessionsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        include_archived=include_archived,
        include_default=include_default,
        include_subagents=include_subagents,
        order=order,
        after_id=after_id,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    agent_profile_id: Union[Unset, str] = UNSET,
    include_archived: Union[Unset, bool] = False,
    include_default: Union[Unset, bool] = False,
    include_subagents: Union[Unset, bool] = False,
    order: Union[Unset, ListProjectAgentSessionsOrder] = "desc",
    after_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[Error, ListProjectAgentSessionsResponse]]:
    """List the project's agent sessions

     Lists the conversation sessions of every agent in the project, ordered by creation time. Each
    agent's default session (the legacy /api/v1 conversation), archived sessions and subagent sessions
    are left out unless requested. Pages are keyset pages: pass the last session of a page as `after_id`
    with the same `order` to read the next one.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (Union[Unset, str]):
        include_archived (Union[Unset, bool]):  Default: False.
        include_default (Union[Unset, bool]):  Default: False.
        include_subagents (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ListProjectAgentSessionsOrder]):  Default: 'desc'.
        after_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListProjectAgentSessionsResponse]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        agent_profile_id=agent_profile_id,
        include_archived=include_archived,
        include_default=include_default,
        include_subagents=include_subagents,
        order=order,
        after_id=after_id,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    agent_profile_id: Union[Unset, str] = UNSET,
    include_archived: Union[Unset, bool] = False,
    include_default: Union[Unset, bool] = False,
    include_subagents: Union[Unset, bool] = False,
    order: Union[Unset, ListProjectAgentSessionsOrder] = "desc",
    after_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[Error, ListProjectAgentSessionsResponse]]:
    """List the project's agent sessions

     Lists the conversation sessions of every agent in the project, ordered by creation time. Each
    agent's default session (the legacy /api/v1 conversation), archived sessions and subagent sessions
    are left out unless requested. Pages are keyset pages: pass the last session of a page as `after_id`
    with the same `order` to read the next one.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (Union[Unset, str]):
        include_archived (Union[Unset, bool]):  Default: False.
        include_default (Union[Unset, bool]):  Default: False.
        include_subagents (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ListProjectAgentSessionsOrder]):  Default: 'desc'.
        after_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListProjectAgentSessionsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        include_archived=include_archived,
        include_default=include_default,
        include_subagents=include_subagents,
        order=order,
        after_id=after_id,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    agent_profile_id: Union[Unset, str] = UNSET,
    include_archived: Union[Unset, bool] = False,
    include_default: Union[Unset, bool] = False,
    include_subagents: Union[Unset, bool] = False,
    order: Union[Unset, ListProjectAgentSessionsOrder] = "desc",
    after_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[Error, ListProjectAgentSessionsResponse]]:
    """List the project's agent sessions

     Lists the conversation sessions of every agent in the project, ordered by creation time. Each
    agent's default session (the legacy /api/v1 conversation), archived sessions and subagent sessions
    are left out unless requested. Pages are keyset pages: pass the last session of a page as `after_id`
    with the same `order` to read the next one.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (Union[Unset, str]):
        include_archived (Union[Unset, bool]):  Default: False.
        include_default (Union[Unset, bool]):  Default: False.
        include_subagents (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ListProjectAgentSessionsOrder]):  Default: 'desc'.
        after_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListProjectAgentSessionsResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            agent_profile_id=agent_profile_id,
            include_archived=include_archived,
            include_default=include_default,
            include_subagents=include_subagents,
            order=order,
            after_id=after_id,
            limit=limit,
        )
    ).parsed
