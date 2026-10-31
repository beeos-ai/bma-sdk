from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.mcpo_auth_start_request import MCPOAuthStartRequest
from ...models.mcpo_auth_start_response import MCPOAuthStartResponse
from ...models.start_secret_mcpo_auth_response_4xx import StartSecretMCPOAuthResponse4XX
from ...models.start_secret_mcpo_auth_response_5xx import StartSecretMCPOAuthResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: MCPOAuthStartRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/secrets/mcp-oauth".format(
            org_id=org_id,
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
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
    ]
]:
    if response.status_code == 201:
        response_201 = MCPOAuthStartResponse.from_dict(response.json())

        return response_201

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
        response_422 = Error.from_dict(response.json())

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
        response_4xx = StartSecretMCPOAuthResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = StartSecretMCPOAuthResponse5XX.from_dict(response.json())

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
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
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
    body: MCPOAuthStartRequest,
) -> Response[
    Union[
        Error,
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
    ]
]:
    """Start MCP OAuth for a new secret

    Args:
        org_id (str):
        body (MCPOAuthStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MCPOAuthStartResponse, StartSecretMCPOAuthResponse4XX, StartSecretMCPOAuthResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPOAuthStartRequest,
) -> Optional[
    Union[
        Error,
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
    ]
]:
    """Start MCP OAuth for a new secret

    Args:
        org_id (str):
        body (MCPOAuthStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MCPOAuthStartResponse, StartSecretMCPOAuthResponse4XX, StartSecretMCPOAuthResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPOAuthStartRequest,
) -> Response[
    Union[
        Error,
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
    ]
]:
    """Start MCP OAuth for a new secret

    Args:
        org_id (str):
        body (MCPOAuthStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MCPOAuthStartResponse, StartSecretMCPOAuthResponse4XX, StartSecretMCPOAuthResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: MCPOAuthStartRequest,
) -> Optional[
    Union[
        Error,
        MCPOAuthStartResponse,
        StartSecretMCPOAuthResponse4XX,
        StartSecretMCPOAuthResponse5XX,
    ]
]:
    """Start MCP OAuth for a new secret

    Args:
        org_id (str):
        body (MCPOAuthStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MCPOAuthStartResponse, StartSecretMCPOAuthResponse4XX, StartSecretMCPOAuthResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
