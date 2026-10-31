from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_mcp_server_tools_response_4xx import ListMCPServerToolsResponse4XX
from ...models.list_mcp_server_tools_response_5xx import ListMCPServerToolsResponse5XX
from ...models.mcp_server_auth_required_error import MCPServerAuthRequiredError
from ...models.mcp_server_tools_request import MCPServerToolsRequest
from ...models.mcp_server_tools_response import MCPServerToolsResponse
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: MCPServerToolsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/mcp-servers/tools".format(
            org_id=org_id,
            project_id=project_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
    ]
]:
    if response.status_code == 200:
        response_200 = MCPServerToolsResponse.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = MCPServerAuthRequiredError.from_dict(response.json())

        return response_422

    if response.status_code == 424:
        response_424 = Error.from_dict(response.json())

        return response_424

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListMCPServerToolsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListMCPServerToolsResponse5XX.from_dict(response.json())

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
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
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
    client: AuthenticatedClient,
    body: MCPServerToolsRequest,
) -> Response[
    Union[
        Error,
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
    ]
]:
    """List an MCP server's tools

     Connects to a remote MCP server over streamable HTTP, negotiates the protocol version (stateless
    `server/discover` first, falling back to the `initialize` handshake for session-based servers), and
    returns the server's `tools/list` result. The request is not stored; use it to preview which tools a
    server exposes before referencing it from an agent config. Authentication mirrors the agent config
    `mcp_servers.<key>.auth` shape and resolves secrets available to the project. When the server does
    not speak MCP, the API responds 422 without an `auth` hint. When the server or its authorization
    server does not respond or fails, including a malformed MCP response or a JSON-RPC internal error
    from the server, the API responds 424; retrying may succeed once the server recovers. When the
    authorization server rejects the configured OAuth secret, the API responds 422 with an `oauth` hint
    so the caller can log in again. When BMA times out reading or storing discovery state, the API
    responds 503. When the server rejects the connection with HTTP 401 or 403, the API probes the
    server's authorization requirements and responds 422 with an `auth` hint — `oauth` when the server
    advertises an OAuth authorization server, `bearer` when it expects a token but advertises no OAuth
    metadata. If that probe fails for a non-transient reason, the 422 carries no `auth` hint.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (MCPServerToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMCPServerToolsResponse4XX, ListMCPServerToolsResponse5XX, MCPServerAuthRequiredError, MCPServerToolsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPServerToolsRequest,
) -> Optional[
    Union[
        Error,
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
    ]
]:
    """List an MCP server's tools

     Connects to a remote MCP server over streamable HTTP, negotiates the protocol version (stateless
    `server/discover` first, falling back to the `initialize` handshake for session-based servers), and
    returns the server's `tools/list` result. The request is not stored; use it to preview which tools a
    server exposes before referencing it from an agent config. Authentication mirrors the agent config
    `mcp_servers.<key>.auth` shape and resolves secrets available to the project. When the server does
    not speak MCP, the API responds 422 without an `auth` hint. When the server or its authorization
    server does not respond or fails, including a malformed MCP response or a JSON-RPC internal error
    from the server, the API responds 424; retrying may succeed once the server recovers. When the
    authorization server rejects the configured OAuth secret, the API responds 422 with an `oauth` hint
    so the caller can log in again. When BMA times out reading or storing discovery state, the API
    responds 503. When the server rejects the connection with HTTP 401 or 403, the API probes the
    server's authorization requirements and responds 422 with an `auth` hint — `oauth` when the server
    advertises an OAuth authorization server, `bearer` when it expects a token but advertises no OAuth
    metadata. If that probe fails for a non-transient reason, the 422 carries no `auth` hint.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (MCPServerToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMCPServerToolsResponse4XX, ListMCPServerToolsResponse5XX, MCPServerAuthRequiredError, MCPServerToolsResponse]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPServerToolsRequest,
) -> Response[
    Union[
        Error,
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
    ]
]:
    """List an MCP server's tools

     Connects to a remote MCP server over streamable HTTP, negotiates the protocol version (stateless
    `server/discover` first, falling back to the `initialize` handshake for session-based servers), and
    returns the server's `tools/list` result. The request is not stored; use it to preview which tools a
    server exposes before referencing it from an agent config. Authentication mirrors the agent config
    `mcp_servers.<key>.auth` shape and resolves secrets available to the project. When the server does
    not speak MCP, the API responds 422 without an `auth` hint. When the server or its authorization
    server does not respond or fails, including a malformed MCP response or a JSON-RPC internal error
    from the server, the API responds 424; retrying may succeed once the server recovers. When the
    authorization server rejects the configured OAuth secret, the API responds 422 with an `oauth` hint
    so the caller can log in again. When BMA times out reading or storing discovery state, the API
    responds 503. When the server rejects the connection with HTTP 401 or 403, the API probes the
    server's authorization requirements and responds 422 with an `auth` hint — `oauth` when the server
    advertises an OAuth authorization server, `bearer` when it expects a token but advertises no OAuth
    metadata. If that probe fails for a non-transient reason, the 422 carries no `auth` hint.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (MCPServerToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMCPServerToolsResponse4XX, ListMCPServerToolsResponse5XX, MCPServerAuthRequiredError, MCPServerToolsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPServerToolsRequest,
) -> Optional[
    Union[
        Error,
        ListMCPServerToolsResponse4XX,
        ListMCPServerToolsResponse5XX,
        MCPServerAuthRequiredError,
        MCPServerToolsResponse,
    ]
]:
    """List an MCP server's tools

     Connects to a remote MCP server over streamable HTTP, negotiates the protocol version (stateless
    `server/discover` first, falling back to the `initialize` handshake for session-based servers), and
    returns the server's `tools/list` result. The request is not stored; use it to preview which tools a
    server exposes before referencing it from an agent config. Authentication mirrors the agent config
    `mcp_servers.<key>.auth` shape and resolves secrets available to the project. When the server does
    not speak MCP, the API responds 422 without an `auth` hint. When the server or its authorization
    server does not respond or fails, including a malformed MCP response or a JSON-RPC internal error
    from the server, the API responds 424; retrying may succeed once the server recovers. When the
    authorization server rejects the configured OAuth secret, the API responds 422 with an `oauth` hint
    so the caller can log in again. When BMA times out reading or storing discovery state, the API
    responds 503. When the server rejects the connection with HTTP 401 or 403, the API probes the
    server's authorization requirements and responds 422 with an `auth` hint — `oauth` when the server
    advertises an OAuth authorization server, `bearer` when it expects a token but advertises no OAuth
    metadata. If that probe fails for a non-transient reason, the 422 carries no `auth` hint.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (MCPServerToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMCPServerToolsResponse4XX, ListMCPServerToolsResponse5XX, MCPServerAuthRequiredError, MCPServerToolsResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
