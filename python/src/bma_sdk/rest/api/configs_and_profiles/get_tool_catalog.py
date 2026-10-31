from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_tool_catalog_response_4xx import GetToolCatalogResponse4XX
from ...models.get_tool_catalog_response_5xx import GetToolCatalogResponse5XX
from ...models.tool_catalog import ToolCatalog
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tool-catalog",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
]:
    if response.status_code == 200:
        response_200 = ToolCatalog.from_dict(response.json())

        return response_200

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
        response_4xx = GetToolCatalogResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetToolCatalogResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
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
) -> Response[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
]:
    """Get tool catalog

     Lists the built-in tools agent configs can use, with each tool's description and permission
    settings, plus the permission modes for custom and MCP tools.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
]:
    """Get tool catalog

     Lists the built-in tools agent configs can use, with each tool's description and permission
    settings, plus the permission modes for custom and MCP tools.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
]:
    """Get tool catalog

     Lists the built-in tools agent configs can use, with each tool's description and permission
    settings, plus the permission modes for custom and MCP tools.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
]:
    """Get tool catalog

     Lists the built-in tools agent configs can use, with each tool's description and permission
    settings, plus the permission modes for custom and MCP tools.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetToolCatalogResponse4XX, GetToolCatalogResponse5XX, ToolCatalog]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
