from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.archive_agent_response_4xx import ArchiveAgentResponse4XX
from ...models.archive_agent_response_5xx import ArchiveAgentResponse5XX
from ...models.current_agent_response import CurrentAgentResponse
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/archive".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
]:
    if response.status_code == 200:
        response_200 = CurrentAgentResponse.from_dict(response.json())

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
        response_4xx = ArchiveAgentResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ArchiveAgentResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
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
    client: AuthenticatedClient,
) -> Response[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
]:
    """Archive agent

     Archives the agent: requests cancellation of its active runtime, cancels queued inputs and affected
    processes, removes its pending wakeup, releases explicit machine bindings, deletes pooled machines
    created for the agent, and deletes cron triggers targeting the agent. Every session of the agent
    that is still active, including the default session, is archived in the same transaction and reports
    `archived` with an `archived_at`. The agent, its sessions and its full event history stay readable
    by id; archived agents and sessions leave active listings. The agent's profile and configuration are
    retained, as are explicitly attached BYO machines. Archiving an already-archived agent is a no-op
    that returns the agent unchanged.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
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
    client: AuthenticatedClient,
) -> Optional[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
]:
    """Archive agent

     Archives the agent: requests cancellation of its active runtime, cancels queued inputs and affected
    processes, removes its pending wakeup, releases explicit machine bindings, deletes pooled machines
    created for the agent, and deletes cron triggers targeting the agent. Every session of the agent
    that is still active, including the default session, is archived in the same transaction and reports
    `archived` with an `archived_at`. The agent, its sessions and its full event history stay readable
    by id; archived agents and sessions leave active listings. The agent's profile and configuration are
    retained, as are explicitly attached BYO machines. Archiving an already-archived agent is a no-op
    that returns the agent unchanged.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
]:
    """Archive agent

     Archives the agent: requests cancellation of its active runtime, cancels queued inputs and affected
    processes, removes its pending wakeup, releases explicit machine bindings, deletes pooled machines
    created for the agent, and deletes cron triggers targeting the agent. Every session of the agent
    that is still active, including the default session, is archived in the same transaction and reports
    `archived` with an `archived_at`. The agent, its sessions and its full event history stay readable
    by id; archived agents and sessions leave active listings. The agent's profile and configuration are
    retained, as are explicitly attached BYO machines. Archiving an already-archived agent is a no-op
    that returns the agent unchanged.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
]:
    """Archive agent

     Archives the agent: requests cancellation of its active runtime, cancels queued inputs and affected
    processes, removes its pending wakeup, releases explicit machine bindings, deletes pooled machines
    created for the agent, and deletes cron triggers targeting the agent. Every session of the agent
    that is still active, including the default session, is archived in the same transaction and reports
    `archived` with an `archived_at`. The agent, its sessions and its full event history stay readable
    by id; archived agents and sessions leave active listings. The agent's profile and configuration are
    retained, as are explicitly attached BYO machines. Archiving an already-archived agent is a no-op
    that returns the agent unchanged.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArchiveAgentResponse4XX, ArchiveAgentResponse5XX, CurrentAgentResponse, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
        )
    ).parsed
