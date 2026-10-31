from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_org_memory_stores_response_4xx import ListOrgMemoryStoresResponse4XX
from ...models.list_org_memory_stores_response_5xx import ListOrgMemoryStoresResponse5XX
from ...models.memory_store_list import MemoryStoreList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    limit: Union[Unset, int] = 50,
    name: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["name"] = name

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/memory-stores".format(
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
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
    ]
]:
    if response.status_code == 200:
        response_200 = MemoryStoreList.from_dict(response.json())

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
        response_4xx = ListOrgMemoryStoresResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListOrgMemoryStoresResponse5XX.from_dict(response.json())

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
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
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
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    name: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
    ]
]:
    """List memory stores across projects

     Lists memory stores in every project of the organization the caller can read. Each store carries its
    project_id. Items are ordered by name, then id.

    Args:
        org_id (str):
        limit (Union[Unset, int]):  Default: 50.
        name (Union[Unset, str]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListOrgMemoryStoresResponse4XX, ListOrgMemoryStoresResponse5XX, MemoryStoreList]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        limit=limit,
        name=name,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    name: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
    ]
]:
    """List memory stores across projects

     Lists memory stores in every project of the organization the caller can read. Each store carries its
    project_id. Items are ordered by name, then id.

    Args:
        org_id (str):
        limit (Union[Unset, int]):  Default: 50.
        name (Union[Unset, str]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListOrgMemoryStoresResponse4XX, ListOrgMemoryStoresResponse5XX, MemoryStoreList]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        limit=limit,
        name=name,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    name: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
    ]
]:
    """List memory stores across projects

     Lists memory stores in every project of the organization the caller can read. Each store carries its
    project_id. Items are ordered by name, then id.

    Args:
        org_id (str):
        limit (Union[Unset, int]):  Default: 50.
        name (Union[Unset, str]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListOrgMemoryStoresResponse4XX, ListOrgMemoryStoresResponse5XX, MemoryStoreList]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        limit=limit,
        name=name,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 50,
    name: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListOrgMemoryStoresResponse4XX,
        ListOrgMemoryStoresResponse5XX,
        MemoryStoreList,
    ]
]:
    """List memory stores across projects

     Lists memory stores in every project of the organization the caller can read. Each store carries its
    project_id. Items are ordered by name, then id.

    Args:
        org_id (str):
        limit (Union[Unset, int]):  Default: 50.
        name (Union[Unset, str]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListOrgMemoryStoresResponse4XX, ListOrgMemoryStoresResponse5XX, MemoryStoreList]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            limit=limit,
            name=name,
            cursor=cursor,
        )
    ).parsed
