from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_org_overview_response_4xx import GetOrgOverviewResponse4XX
from ...models.get_org_overview_response_5xx import GetOrgOverviewResponse5XX
from ...models.org_overview_response import OrgOverviewResponse
from ...types import Response


def _get_kwargs(
    org_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/overview".format(
            org_id=org_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
    ]
]:
    if response.status_code == 200:
        response_200 = OrgOverviewResponse.from_dict(response.json())

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
        response_4xx = GetOrgOverviewResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetOrgOverviewResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
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
) -> Response[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
    ]
]:
    """Get org overview

     Returns the data backing the web app's overview page: the caller's visible projects, the most
    recently active agents, and the most recently updated agent profiles. Internal to the web app and
    subject to change without notice.

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
    ]
]:
    """Get org overview

     Returns the data backing the web app's overview page: the caller's visible projects, the most
    recently active agents, and the most recently updated agent profiles. Internal to the web app and
    subject to change without notice.

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
    ]
]:
    """Get org overview

     Returns the data backing the web app's overview page: the caller's visible projects, the most
    recently active agents, and the most recently updated agent profiles. Internal to the web app and
    subject to change without notice.

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse
    ]
]:
    """Get org overview

     Returns the data backing the web app's overview page: the caller's visible projects, the most
    recently active agents, and the most recently updated agent profiles. Internal to the web app and
    subject to change without notice.

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetOrgOverviewResponse4XX, GetOrgOverviewResponse5XX, OrgOverviewResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
        )
    ).parsed
