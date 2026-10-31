from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_mcp_servers_response import ListMCPServersResponse
from ...models.list_mcp_servers_response_4xx import ListMCPServersResponse4XX
from ...models.list_mcp_servers_response_5xx import ListMCPServersResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: Union[Unset, str] = UNSET,
    remote_url: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["remote_url"] = remote_url

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/mcp-servers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ListMCPServersResponse.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if 400 <= response.status_code <= 499:
        response_4xx = ListMCPServersResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListMCPServersResponse5XX.from_dict(response.json())

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
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
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
    q: Union[Unset, str] = UNSET,
    remote_url: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
    ]
]:
    """Search the MCP server registry

     Search the API's snapshot of the public MCP registry. The snapshot only holds active servers that
    publish a `streamable-http` remote. Results are ranked by relevance when `q` is set, otherwise
    ordered by name.

    Args:
        q (Union[Unset, str]):
        remote_url (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMCPServersResponse, ListMCPServersResponse4XX, ListMCPServersResponse5XX]]
    """

    kwargs = _get_kwargs(
        q=q,
        remote_url=remote_url,
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
    q: Union[Unset, str] = UNSET,
    remote_url: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
    ]
]:
    """Search the MCP server registry

     Search the API's snapshot of the public MCP registry. The snapshot only holds active servers that
    publish a `streamable-http` remote. Results are ranked by relevance when `q` is set, otherwise
    ordered by name.

    Args:
        q (Union[Unset, str]):
        remote_url (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMCPServersResponse, ListMCPServersResponse4XX, ListMCPServersResponse5XX]
    """

    return sync_detailed(
        client=client,
        q=q,
        remote_url=remote_url,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    remote_url: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
    ]
]:
    """Search the MCP server registry

     Search the API's snapshot of the public MCP registry. The snapshot only holds active servers that
    publish a `streamable-http` remote. Results are ranked by relevance when `q` is set, otherwise
    ordered by name.

    Args:
        q (Union[Unset, str]):
        remote_url (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMCPServersResponse, ListMCPServersResponse4XX, ListMCPServersResponse5XX]]
    """

    kwargs = _get_kwargs(
        q=q,
        remote_url=remote_url,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = UNSET,
    remote_url: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListMCPServersResponse,
        ListMCPServersResponse4XX,
        ListMCPServersResponse5XX,
    ]
]:
    """Search the MCP server registry

     Search the API's snapshot of the public MCP registry. The snapshot only holds active servers that
    publish a `streamable-http` remote. Results are ranked by relevance when `q` is set, otherwise
    ordered by name.

    Args:
        q (Union[Unset, str]):
        remote_url (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMCPServersResponse, ListMCPServersResponse4XX, ListMCPServersResponse5XX]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            remote_url=remote_url,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
