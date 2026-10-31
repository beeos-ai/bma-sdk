from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_personal_access_tokens_response import (
    ListPersonalAccessTokensResponse,
)
from ...models.list_personal_access_tokens_response_4xx import (
    ListPersonalAccessTokensResponse4XX,
)
from ...models.list_personal_access_tokens_response_5xx import (
    ListPersonalAccessTokensResponse5XX,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/personal-access-tokens",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ListPersonalAccessTokensResponse.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListPersonalAccessTokensResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListPersonalAccessTokensResponse5XX.from_dict(response.json())

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
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    """List the authenticated user's personal access tokens

     Items are ordered by created_at descending, then id descending.

    Args:
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListPersonalAccessTokensResponse, ListPersonalAccessTokensResponse4XX, ListPersonalAccessTokensResponse5XX]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    """List the authenticated user's personal access tokens

     Items are ordered by created_at descending, then id descending.

    Args:
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListPersonalAccessTokensResponse, ListPersonalAccessTokensResponse4XX, ListPersonalAccessTokensResponse5XX]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    """List the authenticated user's personal access tokens

     Items are ordered by created_at descending, then id descending.

    Args:
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListPersonalAccessTokensResponse, ListPersonalAccessTokensResponse4XX, ListPersonalAccessTokensResponse5XX]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListPersonalAccessTokensResponse,
        ListPersonalAccessTokensResponse4XX,
        ListPersonalAccessTokensResponse5XX,
    ]
]:
    """List the authenticated user's personal access tokens

     Items are ordered by created_at descending, then id descending.

    Args:
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListPersonalAccessTokensResponse, ListPersonalAccessTokensResponse4XX, ListPersonalAccessTokensResponse5XX]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
