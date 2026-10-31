from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.register_daemon_runtime_request import RegisterDaemonRuntimeRequest
from ...models.register_daemon_runtime_response import RegisterDaemonRuntimeResponse
from ...models.register_machine_daemon_runtime_response_4xx import (
    RegisterMachineDaemonRuntimeResponse4XX,
)
from ...models.register_machine_daemon_runtime_response_5xx import (
    RegisterMachineDaemonRuntimeResponse5XX,
)
from ...types import Response


def _get_kwargs(
    *,
    body: RegisterDaemonRuntimeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/runtimes",
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
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
    ]
]:
    if response.status_code == 201:
        response_201 = RegisterDaemonRuntimeResponse.from_dict(response.json())

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

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = RegisterMachineDaemonRuntimeResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = RegisterMachineDaemonRuntimeResponse5XX.from_dict(
            response.json()
        )

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
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
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
    client: AuthenticatedClient,
    body: RegisterDaemonRuntimeRequest,
) -> Response[
    Union[
        Error,
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Register machine daemon runtime

    Args:
        body (RegisterDaemonRuntimeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RegisterDaemonRuntimeResponse, RegisterMachineDaemonRuntimeResponse4XX, RegisterMachineDaemonRuntimeResponse5XX]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RegisterDaemonRuntimeRequest,
) -> Optional[
    Union[
        Error,
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Register machine daemon runtime

    Args:
        body (RegisterDaemonRuntimeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RegisterDaemonRuntimeResponse, RegisterMachineDaemonRuntimeResponse4XX, RegisterMachineDaemonRuntimeResponse5XX]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RegisterDaemonRuntimeRequest,
) -> Response[
    Union[
        Error,
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Register machine daemon runtime

    Args:
        body (RegisterDaemonRuntimeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RegisterDaemonRuntimeResponse, RegisterMachineDaemonRuntimeResponse4XX, RegisterMachineDaemonRuntimeResponse5XX]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RegisterDaemonRuntimeRequest,
) -> Optional[
    Union[
        Error,
        RegisterDaemonRuntimeResponse,
        RegisterMachineDaemonRuntimeResponse4XX,
        RegisterMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Register machine daemon runtime

    Args:
        body (RegisterDaemonRuntimeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RegisterDaemonRuntimeResponse, RegisterMachineDaemonRuntimeResponse4XX, RegisterMachineDaemonRuntimeResponse5XX]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
