from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capture_desktop_screenshot_response_4xx import (
    CaptureDesktopScreenshotResponse4XX,
)
from ...models.capture_desktop_screenshot_response_5xx import (
    CaptureDesktopScreenshotResponse5XX,
)
from ...models.desktop_screenshot import DesktopScreenshot
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/machines/{machine_id}/desktop-sessions/{desktop_session_id}/screenshot".format(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            desktop_session_id=desktop_session_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
    ]
]:
    if response.status_code == 200:
        response_200 = DesktopScreenshot.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = CaptureDesktopScreenshotResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CaptureDesktopScreenshotResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
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
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
    ]
]:
    """Capture the desktop

     Captures the current framebuffer. The image is returned base64-encoded in JSON.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CaptureDesktopScreenshotResponse4XX, CaptureDesktopScreenshotResponse5XX, DesktopScreenshot, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
    ]
]:
    """Capture the desktop

     Captures the current framebuffer. The image is returned base64-encoded in JSON.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CaptureDesktopScreenshotResponse4XX, CaptureDesktopScreenshotResponse5XX, DesktopScreenshot, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
    ]
]:
    """Capture the desktop

     Captures the current framebuffer. The image is returned base64-encoded in JSON.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CaptureDesktopScreenshotResponse4XX, CaptureDesktopScreenshotResponse5XX, DesktopScreenshot, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        CaptureDesktopScreenshotResponse4XX,
        CaptureDesktopScreenshotResponse5XX,
        DesktopScreenshot,
        Error,
    ]
]:
    """Capture the desktop

     Captures the current framebuffer. The image is returned base64-encoded in JSON.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CaptureDesktopScreenshotResponse4XX, CaptureDesktopScreenshotResponse5XX, DesktopScreenshot, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            desktop_session_id=desktop_session_id,
            client=client,
        )
    ).parsed
