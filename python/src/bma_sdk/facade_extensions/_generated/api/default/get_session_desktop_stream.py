from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.desktop_stream import DesktopStream
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    desktop_session_id: str,
    ttl_seconds: Union[Unset, int] = UNSET,
    origin: Union[Unset, str] = UNSET,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_project_id, Unset):
        headers["x-bma-project-id"] = x_bma_project_id

    params: dict[str, Any] = {}

    params["desktop_session_id"] = desktop_session_id

    params["ttl_seconds"] = ttl_seconds

    params["origin"] = origin

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions/{session_id}/desktop/stream".format(
            session_id=session_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DesktopStream, ErrorEnvelope]:
    if response.status_code == 200:
        response_200 = DesktopStream.from_dict(response.json())

        return response_200

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DesktopStream, ErrorEnvelope]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    desktop_session_id: str,
    ttl_seconds: Union[Unset, int] = UNSET,
    origin: Union[Unset, str] = UNSET,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[DesktopStream, ErrorEnvelope]]:
    """Mint a desktop watch ticket for a session (BMA extension)

     Returns a short-lived, single-use, origin-bound watch ticket and the
    WebSocket endpoint of the desktop session attached to the session's
    machine. The browser connects to `url` with `subprotocol` and the
    ticket; the tenant API key never reaches the browser.

    Args:
        session_id (str):
        desktop_session_id (str):
        ttl_seconds (Union[Unset, int]):
        origin (Union[Unset, str]):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DesktopStream, ErrorEnvelope]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        desktop_session_id=desktop_session_id,
        ttl_seconds=ttl_seconds,
        origin=origin,
        x_bma_project_id=x_bma_project_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    desktop_session_id: str,
    ttl_seconds: Union[Unset, int] = UNSET,
    origin: Union[Unset, str] = UNSET,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DesktopStream, ErrorEnvelope]]:
    """Mint a desktop watch ticket for a session (BMA extension)

     Returns a short-lived, single-use, origin-bound watch ticket and the
    WebSocket endpoint of the desktop session attached to the session's
    machine. The browser connects to `url` with `subprotocol` and the
    ticket; the tenant API key never reaches the browser.

    Args:
        session_id (str):
        desktop_session_id (str):
        ttl_seconds (Union[Unset, int]):
        origin (Union[Unset, str]):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DesktopStream, ErrorEnvelope]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        desktop_session_id=desktop_session_id,
        ttl_seconds=ttl_seconds,
        origin=origin,
        x_bma_project_id=x_bma_project_id,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    desktop_session_id: str,
    ttl_seconds: Union[Unset, int] = UNSET,
    origin: Union[Unset, str] = UNSET,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[DesktopStream, ErrorEnvelope]]:
    """Mint a desktop watch ticket for a session (BMA extension)

     Returns a short-lived, single-use, origin-bound watch ticket and the
    WebSocket endpoint of the desktop session attached to the session's
    machine. The browser connects to `url` with `subprotocol` and the
    ticket; the tenant API key never reaches the browser.

    Args:
        session_id (str):
        desktop_session_id (str):
        ttl_seconds (Union[Unset, int]):
        origin (Union[Unset, str]):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DesktopStream, ErrorEnvelope]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        desktop_session_id=desktop_session_id,
        ttl_seconds=ttl_seconds,
        origin=origin,
        x_bma_project_id=x_bma_project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    desktop_session_id: str,
    ttl_seconds: Union[Unset, int] = UNSET,
    origin: Union[Unset, str] = UNSET,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DesktopStream, ErrorEnvelope]]:
    """Mint a desktop watch ticket for a session (BMA extension)

     Returns a short-lived, single-use, origin-bound watch ticket and the
    WebSocket endpoint of the desktop session attached to the session's
    machine. The browser connects to `url` with `subprotocol` and the
    ticket; the tenant API key never reaches the browser.

    Args:
        session_id (str):
        desktop_session_id (str):
        ttl_seconds (Union[Unset, int]):
        origin (Union[Unset, str]):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DesktopStream, ErrorEnvelope]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            desktop_session_id=desktop_session_id,
            ttl_seconds=ttl_seconds,
            origin=origin,
            x_bma_project_id=x_bma_project_id,
        )
    ).parsed
