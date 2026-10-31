from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_agent_machines_response import ListAgentMachinesResponse
from ...models.list_agent_machines_response_4xx import ListAgentMachinesResponse4XX
from ...models.list_agent_machines_response_5xx import ListAgentMachinesResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/machines".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ListAgentMachinesResponse.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListAgentMachinesResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListAgentMachinesResponse5XX.from_dict(response.json())

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
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
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
    client: AuthenticatedClient,
) -> Response[
    Union[
        Error,
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
    ]
]:
    """List an agent's pooled machines

     Lists the pooled machines attached to an agent, in binding creation order, with each machine's kind.
    A persistent machine is kept for a person (for example a purchased BMA computer) and is never
    deleted for being idle; an ephemeral machine serves turns and is deleted after its idle window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentMachinesResponse, ListAgentMachinesResponse4XX, ListAgentMachinesResponse5XX]]
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
    Union[
        Error,
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
    ]
]:
    """List an agent's pooled machines

     Lists the pooled machines attached to an agent, in binding creation order, with each machine's kind.
    A persistent machine is kept for a person (for example a purchased BMA computer) and is never
    deleted for being idle; an ephemeral machine serves turns and is deleted after its idle window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentMachinesResponse, ListAgentMachinesResponse4XX, ListAgentMachinesResponse5XX]
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
    Union[
        Error,
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
    ]
]:
    """List an agent's pooled machines

     Lists the pooled machines attached to an agent, in binding creation order, with each machine's kind.
    A persistent machine is kept for a person (for example a purchased BMA computer) and is never
    deleted for being idle; an ephemeral machine serves turns and is deleted after its idle window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListAgentMachinesResponse, ListAgentMachinesResponse4XX, ListAgentMachinesResponse5XX]]
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
    Union[
        Error,
        ListAgentMachinesResponse,
        ListAgentMachinesResponse4XX,
        ListAgentMachinesResponse5XX,
    ]
]:
    """List an agent's pooled machines

     Lists the pooled machines attached to an agent, in binding creation order, with each machine's kind.
    A persistent machine is kept for a person (for example a purchased BMA computer) and is never
    deleted for being idle; an ephemeral machine serves turns and is deleted after its idle window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListAgentMachinesResponse, ListAgentMachinesResponse4XX, ListAgentMachinesResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
        )
    ).parsed
