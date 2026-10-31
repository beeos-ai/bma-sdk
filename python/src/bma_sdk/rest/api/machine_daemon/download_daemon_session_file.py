from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.download_daemon_session_file_response_4xx import (
    DownloadDaemonSessionFileResponse4XX,
)
from ...models.download_daemon_session_file_response_5xx import (
    DownloadDaemonSessionFileResponse5XX,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    process_id: str,
    resource_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/daemon/processes/{process_id}/session-files/{resource_id}/content".format(
            process_id=process_id,
            resource_id=resource_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
        Error,
    ]
]:
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if 400 <= response.status_code <= 499:
        response_4xx = DownloadDaemonSessionFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DownloadDaemonSessionFileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
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
    process_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
        Error,
    ]
]:
    """Download a session file a process sees

    Args:
        process_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonSessionFileResponse4XX, DownloadDaemonSessionFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        resource_id=resource_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    process_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
        Error,
    ]
]:
    """Download a session file a process sees

    Args:
        process_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonSessionFileResponse4XX, DownloadDaemonSessionFileResponse5XX, Error]
    """

    return sync_detailed(
        process_id=process_id,
        resource_id=resource_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    process_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
        Error,
    ]
]:
    """Download a session file a process sees

    Args:
        process_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonSessionFileResponse4XX, DownloadDaemonSessionFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        resource_id=resource_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DownloadDaemonSessionFileResponse4XX,
        DownloadDaemonSessionFileResponse5XX,
        Error,
    ]
]:
    """Download a session file a process sees

    Args:
        process_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonSessionFileResponse4XX, DownloadDaemonSessionFileResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            resource_id=resource_id,
            client=client,
        )
    ).parsed
