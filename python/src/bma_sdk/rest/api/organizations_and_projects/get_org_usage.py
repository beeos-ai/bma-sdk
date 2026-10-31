import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_org_usage_response_4xx import GetOrgUsageResponse4XX
from ...models.get_org_usage_response_5xx import GetOrgUsageResponse5XX
from ...models.usage_report import UsageReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_project_ids: Union[Unset, list[str]] = UNSET,
    exclude_project_ids: Union[Unset, list[str]] = UNSET,
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

    json_include_project_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(include_project_ids, Unset):
        json_include_project_ids = include_project_ids

    params["include_project_ids"] = json_include_project_ids

    json_exclude_project_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(exclude_project_ids, Unset):
        json_exclude_project_ids = exclude_project_ids

    params["exclude_project_ids"] = json_exclude_project_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/usage".format(
            org_id=org_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
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
        response_4xx = GetOrgUsageResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetOrgUsageResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
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
    include_project_ids: Union[Unset, list[str]] = UNSET,
    exclude_project_ids: Union[Unset, list[str]] = UNSET,
) -> Response[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
]:
    """Get org usage

     Tallies model token usage and provider-reported cost across every project the caller can read in the
    organization, broken down by configured model. Optionally limits the tally to a time window or to a
    subset of those projects; including a project the caller can't read is not found.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_project_ids (Union[Unset, list[str]]):
        exclude_project_ids (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        since=since,
        until=until,
        include_project_ids=include_project_ids,
        exclude_project_ids=exclude_project_ids,
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
    include_project_ids: Union[Unset, list[str]] = UNSET,
    exclude_project_ids: Union[Unset, list[str]] = UNSET,
) -> Optional[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
]:
    """Get org usage

     Tallies model token usage and provider-reported cost across every project the caller can read in the
    organization, broken down by configured model. Optionally limits the tally to a time window or to a
    subset of those projects; including a project the caller can't read is not found.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_project_ids (Union[Unset, list[str]]):
        exclude_project_ids (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        since=since,
        until=until,
        include_project_ids=include_project_ids,
        exclude_project_ids=exclude_project_ids,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_project_ids: Union[Unset, list[str]] = UNSET,
    exclude_project_ids: Union[Unset, list[str]] = UNSET,
) -> Response[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
]:
    """Get org usage

     Tallies model token usage and provider-reported cost across every project the caller can read in the
    organization, broken down by configured model. Optionally limits the tally to a time window or to a
    subset of those projects; including a project the caller can't read is not found.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_project_ids (Union[Unset, list[str]]):
        exclude_project_ids (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        since=since,
        until=until,
        include_project_ids=include_project_ids,
        exclude_project_ids=exclude_project_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
    include_project_ids: Union[Unset, list[str]] = UNSET,
    exclude_project_ids: Union[Unset, list[str]] = UNSET,
) -> Optional[
    Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
]:
    """Get org usage

     Tallies model token usage and provider-reported cost across every project the caller can read in the
    organization, broken down by configured model. Optionally limits the tally to a time window or to a
    subset of those projects; including a project the caller can't read is not found.

    Args:
        org_id (str):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):
        include_project_ids (Union[Unset, list[str]]):
        exclude_project_ids (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgUsageResponse4XX, GetOrgUsageResponse5XX, UsageReport]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            since=since,
            until=until,
            include_project_ids=include_project_ids,
            exclude_project_ids=exclude_project_ids,
        )
    ).parsed
