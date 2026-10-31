from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_cron_triggers_response import ListCronTriggersResponse
from ...models.list_cron_triggers_response_4xx import ListCronTriggersResponse4XX
from ...models.list_cron_triggers_response_5xx import ListCronTriggersResponse5XX
from ...models.resource_list_sort import ResourceListSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    name: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
    agent_profile_id: Union[Unset, str] = UNSET,
    integration_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["name"] = name

    params["agent_id"] = agent_id

    params["agent_profile_id"] = agent_profile_id

    params["integration_id"] = integration_id

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/cron-triggers".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ListCronTriggersResponse.from_dict(response.json())

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
        response_4xx = ListCronTriggersResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListCronTriggersResponse5XX.from_dict(response.json())

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
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
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
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
    agent_profile_id: Union[Unset, str] = UNSET,
    integration_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
    ]
]:
    """List cron triggers

     Lists the project's cron triggers, newest first by default, filterable by name, agent, profile, or
    integration. Each item includes its schedule and next_fire_at.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        agent_id (Union[Unset, str]):
        agent_profile_id (Union[Unset, str]):
        integration_id (Union[Unset, str]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListCronTriggersResponse, ListCronTriggersResponse4XX, ListCronTriggersResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        name=name,
        agent_id=agent_id,
        agent_profile_id=agent_profile_id,
        integration_id=integration_id,
        sort=sort,
        limit=limit,
        cursor=cursor,
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
    name: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
    agent_profile_id: Union[Unset, str] = UNSET,
    integration_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
    ]
]:
    """List cron triggers

     Lists the project's cron triggers, newest first by default, filterable by name, agent, profile, or
    integration. Each item includes its schedule and next_fire_at.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        agent_id (Union[Unset, str]):
        agent_profile_id (Union[Unset, str]):
        integration_id (Union[Unset, str]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListCronTriggersResponse, ListCronTriggersResponse4XX, ListCronTriggersResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        name=name,
        agent_id=agent_id,
        agent_profile_id=agent_profile_id,
        integration_id=integration_id,
        sort=sort,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
    agent_profile_id: Union[Unset, str] = UNSET,
    integration_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
    ]
]:
    """List cron triggers

     Lists the project's cron triggers, newest first by default, filterable by name, agent, profile, or
    integration. Each item includes its schedule and next_fire_at.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        agent_id (Union[Unset, str]):
        agent_profile_id (Union[Unset, str]):
        integration_id (Union[Unset, str]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListCronTriggersResponse, ListCronTriggersResponse4XX, ListCronTriggersResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        name=name,
        agent_id=agent_id,
        agent_profile_id=agent_profile_id,
        integration_id=integration_id,
        sort=sort,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
    agent_profile_id: Union[Unset, str] = UNSET,
    integration_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListCronTriggersResponse,
        ListCronTriggersResponse4XX,
        ListCronTriggersResponse5XX,
    ]
]:
    """List cron triggers

     Lists the project's cron triggers, newest first by default, filterable by name, agent, profile, or
    integration. Each item includes its schedule and next_fire_at.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        agent_id (Union[Unset, str]):
        agent_profile_id (Union[Unset, str]):
        integration_id (Union[Unset, str]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListCronTriggersResponse, ListCronTriggersResponse4XX, ListCronTriggersResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            name=name,
            agent_id=agent_id,
            agent_profile_id=agent_profile_id,
            integration_id=integration_id,
            sort=sort,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
