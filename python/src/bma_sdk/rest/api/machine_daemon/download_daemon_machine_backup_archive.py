from http import HTTPStatus
from io import BytesIO
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.download_daemon_machine_backup_archive_response_4xx import (
    DownloadDaemonMachineBackupArchiveResponse4XX,
)
from ...models.download_daemon_machine_backup_archive_response_5xx import (
    DownloadDaemonMachineBackupArchiveResponse5XX,
)
from ...models.error import Error
from ...types import File, Response


def _get_kwargs(
    backup_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/daemon/machine-backups/{backup_id}/archive".format(
            backup_id=backup_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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
        response_4xx = DownloadDaemonMachineBackupArchiveResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DownloadDaemonMachineBackupArchiveResponse5XX.from_dict(
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
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    backup_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    """Download a machine workspace backup archive

     Requires machine daemon authentication and a ready backup of that machine.

    Args:
        backup_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonMachineBackupArchiveResponse4XX, DownloadDaemonMachineBackupArchiveResponse5XX, Error, File]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    backup_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    """Download a machine workspace backup archive

     Requires machine daemon authentication and a ready backup of that machine.

    Args:
        backup_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonMachineBackupArchiveResponse4XX, DownloadDaemonMachineBackupArchiveResponse5XX, Error, File]
    """

    return sync_detailed(
        backup_id=backup_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    backup_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    """Download a machine workspace backup archive

     Requires machine daemon authentication and a ready backup of that machine.

    Args:
        backup_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonMachineBackupArchiveResponse4XX, DownloadDaemonMachineBackupArchiveResponse5XX, Error, File]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    backup_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DownloadDaemonMachineBackupArchiveResponse4XX,
        DownloadDaemonMachineBackupArchiveResponse5XX,
        Error,
        File,
    ]
]:
    """Download a machine workspace backup archive

     Requires machine daemon authentication and a ready backup of that machine.

    Args:
        backup_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonMachineBackupArchiveResponse4XX, DownloadDaemonMachineBackupArchiveResponse5XX, Error, File]
    """

    return (
        await asyncio_detailed(
            backup_id=backup_id,
            client=client,
        )
    ).parsed
