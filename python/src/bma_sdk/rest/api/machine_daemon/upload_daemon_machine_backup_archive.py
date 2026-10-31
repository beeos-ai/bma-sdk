from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daemon_machine_backup_archive import DaemonMachineBackupArchive
from ...models.error import Error
from ...models.upload_daemon_machine_backup_archive_response_4xx import (
    UploadDaemonMachineBackupArchiveResponse4XX,
)
from ...models.upload_daemon_machine_backup_archive_response_5xx import (
    UploadDaemonMachineBackupArchiveResponse5XX,
)
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    backup_id: str,
    *,
    body: File,
    x_bma_backup_fingerprint: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_backup_fingerprint, Unset):
        headers["X-BMA-Backup-Fingerprint"] = x_bma_backup_fingerprint

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/daemon/machine-backups/{backup_id}/archive".format(
            backup_id=backup_id,
        ),
    }

    _kwargs["content"] = body.payload

    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = DaemonMachineBackupArchive.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = UploadDaemonMachineBackupArchiveResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UploadDaemonMachineBackupArchiveResponse5XX.from_dict(
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
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
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
    body: File,
    x_bma_backup_fingerprint: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
    ]
]:
    """Upload a machine workspace backup archive

     Requires machine daemon authentication and an uploading backup of that machine. The body is the
    tar+zstd archive, streamed without a known length.

    Args:
        backup_id (str):
        x_bma_backup_fingerprint (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonMachineBackupArchive, Error, UploadDaemonMachineBackupArchiveResponse4XX, UploadDaemonMachineBackupArchiveResponse5XX]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
        body=body,
        x_bma_backup_fingerprint=x_bma_backup_fingerprint,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    x_bma_backup_fingerprint: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
    ]
]:
    """Upload a machine workspace backup archive

     Requires machine daemon authentication and an uploading backup of that machine. The body is the
    tar+zstd archive, streamed without a known length.

    Args:
        backup_id (str):
        x_bma_backup_fingerprint (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonMachineBackupArchive, Error, UploadDaemonMachineBackupArchiveResponse4XX, UploadDaemonMachineBackupArchiveResponse5XX]
    """

    return sync_detailed(
        backup_id=backup_id,
        client=client,
        body=body,
        x_bma_backup_fingerprint=x_bma_backup_fingerprint,
    ).parsed


async def asyncio_detailed(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    x_bma_backup_fingerprint: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
    ]
]:
    """Upload a machine workspace backup archive

     Requires machine daemon authentication and an uploading backup of that machine. The body is the
    tar+zstd archive, streamed without a known length.

    Args:
        backup_id (str):
        x_bma_backup_fingerprint (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonMachineBackupArchive, Error, UploadDaemonMachineBackupArchiveResponse4XX, UploadDaemonMachineBackupArchiveResponse5XX]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
        body=body,
        x_bma_backup_fingerprint=x_bma_backup_fingerprint,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    x_bma_backup_fingerprint: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        DaemonMachineBackupArchive,
        Error,
        UploadDaemonMachineBackupArchiveResponse4XX,
        UploadDaemonMachineBackupArchiveResponse5XX,
    ]
]:
    """Upload a machine workspace backup archive

     Requires machine daemon authentication and an uploading backup of that machine. The body is the
    tar+zstd archive, streamed without a known length.

    Args:
        backup_id (str):
        x_bma_backup_fingerprint (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonMachineBackupArchive, Error, UploadDaemonMachineBackupArchiveResponse4XX, UploadDaemonMachineBackupArchiveResponse5XX]
    """

    return (
        await asyncio_detailed(
            backup_id=backup_id,
            client=client,
            body=body,
            x_bma_backup_fingerprint=x_bma_backup_fingerprint,
        )
    ).parsed
