import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_agent_profile_usage_response_4xx import (
    GetAgentProfileUsageResponse4XX,
)
from ...models.get_agent_profile_usage_response_5xx import (
    GetAgentProfileUsageResponse5XX,
)
from ...models.usage_report import UsageReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_subagents: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_since: Union[Unset, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_until: Union[Unset, str] = UNSET
    if not isinstance(until, Unset):
        json_until = until.isoformat()
    params["until"] = json_until

    params["include_subagents"] = include_subagents

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-profiles/{agent_profile_id}/usage".format(
            org_id=org_id,
            project_id=project_id,
            agent_profile_id=agent_profile_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
    ]
]:
    if response.status_code == 200:
        response_200 = UsageReport.from_dict(response.json())

        return response_200

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
        response_4xx = GetAgentProfileUsageResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetAgentProfileUsageResponse5XX.from_dict(response.json())

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
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
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
    agent_profile_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_subagents: Union[Unset, bool] = UNSET,
) -> Response[
    Union[
        Error,
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
    ]
]:
    """Get agent profile usage

     Tallies model token usage and provider-reported cost across the top-level agents launched from this
    profile, broken down by configured model. Usage from subagents those agents spawned is included only
    when `include_subagents` is true. Optionally limits the tally to a time window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_profile_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_subagents (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetAgentProfileUsageResponse4XX, GetAgentProfileUsageResponse5XX, UsageReport]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        since=since,
        until=until,
        include_subagents=include_subagents,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_subagents: Union[Unset, bool] = UNSET,
) -> Optional[
    Union[
        Error,
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
    ]
]:
    """Get agent profile usage

     Tallies model token usage and provider-reported cost across the top-level agents launched from this
    profile, broken down by configured model. Usage from subagents those agents spawned is included only
    when `include_subagents` is true. Optionally limits the tally to a time window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_profile_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_subagents (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetAgentProfileUsageResponse4XX, GetAgentProfileUsageResponse5XX, UsageReport]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        client=client,
        since=since,
        until=until,
        include_subagents=include_subagents,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_subagents: Union[Unset, bool] = UNSET,
) -> Response[
    Union[
        Error,
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
    ]
]:
    """Get agent profile usage

     Tallies model token usage and provider-reported cost across the top-level agents launched from this
    profile, broken down by configured model. Usage from subagents those agents spawned is included only
    when `include_subagents` is true. Optionally limits the tally to a time window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_profile_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_subagents (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetAgentProfileUsageResponse4XX, GetAgentProfileUsageResponse5XX, UsageReport]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        since=since,
        until=until,
        include_subagents=include_subagents,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_subagents: Union[Unset, bool] = UNSET,
) -> Optional[
    Union[
        Error,
        GetAgentProfileUsageResponse4XX,
        GetAgentProfileUsageResponse5XX,
        UsageReport,
    ]
]:
    """Get agent profile usage

     Tallies model token usage and provider-reported cost across the top-level agents launched from this
    profile, broken down by configured model. Usage from subagents those agents spawned is included only
    when `include_subagents` is true. Optionally limits the tally to a time window.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_profile_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_subagents (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetAgentProfileUsageResponse4XX, GetAgentProfileUsageResponse5XX, UsageReport]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_profile_id=agent_profile_id,
            client=client,
            since=since,
            until=until,
            include_subagents=include_subagents,
        )
    ).parsed
