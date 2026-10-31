import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_org_usage_timeseries_response_4xx import (
    GetOrgUsageTimeseriesResponse4XX,
)
from ...models.get_org_usage_timeseries_response_5xx import (
    GetOrgUsageTimeseriesResponse5XX,
)
from ...models.usage_timeseries import UsageTimeseries
from ...models.usage_timeseries_group_by import (
    UsageTimeseriesGroupBy,
)
from ...models.usage_timeseries_interval import (
    UsageTimeseriesInterval,
)
from ...models.usage_timeseries_metric import (
    UsageTimeseriesMetric,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    timezone: Union[Unset, str] = "UTC",
    interval: Union[Unset, UsageTimeseriesInterval] = UNSET,
    metric: Union[Unset, UsageTimeseriesMetric] = UNSET,
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET,
    group_limit: Union[Unset, int] = 8,
    project_ids: Union[Unset, list[str]] = UNSET,
    agent_profile_ids: Union[Unset, list[str]] = UNSET,
    include_subagents: Union[Unset, bool] = False,
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

    params["timezone"] = timezone

    json_interval: Union[Unset, str] = UNSET
    if not isinstance(interval, Unset):
        json_interval = interval

    params["interval"] = json_interval

    json_metric: Union[Unset, str] = UNSET
    if not isinstance(metric, Unset):
        json_metric = metric

    params["metric"] = json_metric

    json_group_by: Union[Unset, str] = UNSET
    if not isinstance(group_by, Unset):
        json_group_by = group_by

    params["group_by"] = json_group_by

    params["group_limit"] = group_limit

    json_project_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(project_ids, Unset):
        json_project_ids = project_ids

    params["project_ids"] = json_project_ids

    json_agent_profile_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(agent_profile_ids, Unset):
        json_agent_profile_ids = agent_profile_ids

    params["agent_profile_ids"] = json_agent_profile_ids

    params["include_subagents"] = include_subagents

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/usage/timeseries".format(
            org_id=org_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
    ]
]:
    if response.status_code == 200:
        response_200 = UsageTimeseries.from_dict(response.json())

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
        response_4xx = GetOrgUsageTimeseriesResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetOrgUsageTimeseriesResponse5XX.from_dict(response.json())

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
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
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
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    timezone: Union[Unset, str] = "UTC",
    interval: Union[Unset, UsageTimeseriesInterval] = UNSET,
    metric: Union[Unset, UsageTimeseriesMetric] = UNSET,
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET,
    group_limit: Union[Unset, int] = 8,
    project_ids: Union[Unset, list[str]] = UNSET,
    agent_profile_ids: Union[Unset, list[str]] = UNSET,
    include_subagents: Union[Unset, bool] = False,
) -> Response[
    Union[
        Error,
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
    ]
]:
    """Get usage timeseries

     Buckets model usage over time for one metric, optionally broken down by configured model or agent
    profile. Covers every project the caller can read in the organization; `project_ids` and
    `agent_profile_ids` narrow that scope. Buckets are calendar days, weeks (starting Monday), or months
    in `timezone`.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        timezone (Union[Unset, str]):  Default: 'UTC'.
        interval (Union[Unset, UsageTimeseriesInterval]):
        metric (Union[Unset, UsageTimeseriesMetric]): `sum_tokens` is input plus output tokens.
            `sum_cost` is provider-reported cost in USD. `count_model_calls` counts model calls that
            recorded usage.
        group_by (Union[Unset, UsageTimeseriesGroupBy]):
        group_limit (Union[Unset, int]):  Default: 8.
        project_ids (Union[Unset, list[str]]):
        agent_profile_ids (Union[Unset, list[str]]):
        include_subagents (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgUsageTimeseriesResponse4XX, GetOrgUsageTimeseriesResponse5XX, UsageTimeseries]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        since=since,
        until=until,
        timezone=timezone,
        interval=interval,
        metric=metric,
        group_by=group_by,
        group_limit=group_limit,
        project_ids=project_ids,
        agent_profile_ids=agent_profile_ids,
        include_subagents=include_subagents,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    timezone: Union[Unset, str] = "UTC",
    interval: Union[Unset, UsageTimeseriesInterval] = UNSET,
    metric: Union[Unset, UsageTimeseriesMetric] = UNSET,
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET,
    group_limit: Union[Unset, int] = 8,
    project_ids: Union[Unset, list[str]] = UNSET,
    agent_profile_ids: Union[Unset, list[str]] = UNSET,
    include_subagents: Union[Unset, bool] = False,
) -> Optional[
    Union[
        Error,
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
    ]
]:
    """Get usage timeseries

     Buckets model usage over time for one metric, optionally broken down by configured model or agent
    profile. Covers every project the caller can read in the organization; `project_ids` and
    `agent_profile_ids` narrow that scope. Buckets are calendar days, weeks (starting Monday), or months
    in `timezone`.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        timezone (Union[Unset, str]):  Default: 'UTC'.
        interval (Union[Unset, UsageTimeseriesInterval]):
        metric (Union[Unset, UsageTimeseriesMetric]): `sum_tokens` is input plus output tokens.
            `sum_cost` is provider-reported cost in USD. `count_model_calls` counts model calls that
            recorded usage.
        group_by (Union[Unset, UsageTimeseriesGroupBy]):
        group_limit (Union[Unset, int]):  Default: 8.
        project_ids (Union[Unset, list[str]]):
        agent_profile_ids (Union[Unset, list[str]]):
        include_subagents (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgUsageTimeseriesResponse4XX, GetOrgUsageTimeseriesResponse5XX, UsageTimeseries]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        since=since,
        until=until,
        timezone=timezone,
        interval=interval,
        metric=metric,
        group_by=group_by,
        group_limit=group_limit,
        project_ids=project_ids,
        agent_profile_ids=agent_profile_ids,
        include_subagents=include_subagents,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    timezone: Union[Unset, str] = "UTC",
    interval: Union[Unset, UsageTimeseriesInterval] = UNSET,
    metric: Union[Unset, UsageTimeseriesMetric] = UNSET,
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET,
    group_limit: Union[Unset, int] = 8,
    project_ids: Union[Unset, list[str]] = UNSET,
    agent_profile_ids: Union[Unset, list[str]] = UNSET,
    include_subagents: Union[Unset, bool] = False,
) -> Response[
    Union[
        Error,
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
    ]
]:
    """Get usage timeseries

     Buckets model usage over time for one metric, optionally broken down by configured model or agent
    profile. Covers every project the caller can read in the organization; `project_ids` and
    `agent_profile_ids` narrow that scope. Buckets are calendar days, weeks (starting Monday), or months
    in `timezone`.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        timezone (Union[Unset, str]):  Default: 'UTC'.
        interval (Union[Unset, UsageTimeseriesInterval]):
        metric (Union[Unset, UsageTimeseriesMetric]): `sum_tokens` is input plus output tokens.
            `sum_cost` is provider-reported cost in USD. `count_model_calls` counts model calls that
            recorded usage.
        group_by (Union[Unset, UsageTimeseriesGroupBy]):
        group_limit (Union[Unset, int]):  Default: 8.
        project_ids (Union[Unset, list[str]]):
        agent_profile_ids (Union[Unset, list[str]]):
        include_subagents (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgUsageTimeseriesResponse4XX, GetOrgUsageTimeseriesResponse5XX, UsageTimeseries]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        since=since,
        until=until,
        timezone=timezone,
        interval=interval,
        metric=metric,
        group_by=group_by,
        group_limit=group_limit,
        project_ids=project_ids,
        agent_profile_ids=agent_profile_ids,
        include_subagents=include_subagents,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    timezone: Union[Unset, str] = "UTC",
    interval: Union[Unset, UsageTimeseriesInterval] = UNSET,
    metric: Union[Unset, UsageTimeseriesMetric] = UNSET,
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET,
    group_limit: Union[Unset, int] = 8,
    project_ids: Union[Unset, list[str]] = UNSET,
    agent_profile_ids: Union[Unset, list[str]] = UNSET,
    include_subagents: Union[Unset, bool] = False,
) -> Optional[
    Union[
        Error,
        GetOrgUsageTimeseriesResponse4XX,
        GetOrgUsageTimeseriesResponse5XX,
        UsageTimeseries,
    ]
]:
    """Get usage timeseries

     Buckets model usage over time for one metric, optionally broken down by configured model or agent
    profile. Covers every project the caller can read in the organization; `project_ids` and
    `agent_profile_ids` narrow that scope. Buckets are calendar days, weeks (starting Monday), or months
    in `timezone`.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        timezone (Union[Unset, str]):  Default: 'UTC'.
        interval (Union[Unset, UsageTimeseriesInterval]):
        metric (Union[Unset, UsageTimeseriesMetric]): `sum_tokens` is input plus output tokens.
            `sum_cost` is provider-reported cost in USD. `count_model_calls` counts model calls that
            recorded usage.
        group_by (Union[Unset, UsageTimeseriesGroupBy]):
        group_limit (Union[Unset, int]):  Default: 8.
        project_ids (Union[Unset, list[str]]):
        agent_profile_ids (Union[Unset, list[str]]):
        include_subagents (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgUsageTimeseriesResponse4XX, GetOrgUsageTimeseriesResponse5XX, UsageTimeseries]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            since=since,
            until=until,
            timezone=timezone,
            interval=interval,
            metric=metric,
            group_by=group_by,
            group_limit=group_limit,
            project_ids=project_ids,
            agent_profile_ids=agent_profile_ids,
            include_subagents=include_subagents,
        )
    ).parsed
