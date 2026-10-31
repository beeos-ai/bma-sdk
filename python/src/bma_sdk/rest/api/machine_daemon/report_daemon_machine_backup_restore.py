from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daemon_machine_backup_restore_result import (
    DaemonMachineBackupRestoreResult,
)
from ...models.error import Error
from ...models.report_daemon_machine_backup_restore_response_4xx import (
    ReportDaemonMachineBackupRestoreResponse4XX,
)
from ...models.report_daemon_machine_backup_restore_response_5xx import (
    ReportDaemonMachineBackupRestoreResponse5XX,
)
from ...types import Response


def _get_kwargs(
    backup_id: str,
    *,
    body: DaemonMachineBackupRestoreResult,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/machine-backups/{backup_id}/restore-result".format(
            backup_id=backup_id,
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
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
    ]
]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
        response_4xx = ReportDaemonMachineBackupRestoreResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ReportDaemonMachineBackupRestoreResponse5XX.from_dict(
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
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
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
    body: DaemonMachineBackupRestoreResult,
) -> Response[
    Union[
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
    ]
]:
    """Report the outcome of a pending workspace restore

    Args:
        backup_id (str):
        body (DaemonMachineBackupRestoreResult):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ReportDaemonMachineBackupRestoreResponse4XX, ReportDaemonMachineBackupRestoreResponse5XX]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: DaemonMachineBackupRestoreResult,
) -> Optional[
    Union[
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
    ]
]:
    """Report the outcome of a pending workspace restore

    Args:
        backup_id (str):
        body (DaemonMachineBackupRestoreResult):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ReportDaemonMachineBackupRestoreResponse4XX, ReportDaemonMachineBackupRestoreResponse5XX]
    """

    return sync_detailed(
        backup_id=backup_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: DaemonMachineBackupRestoreResult,
) -> Response[
    Union[
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
    ]
]:
    """Report the outcome of a pending workspace restore

    Args:
        backup_id (str):
        body (DaemonMachineBackupRestoreResult):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ReportDaemonMachineBackupRestoreResponse4XX, ReportDaemonMachineBackupRestoreResponse5XX]]
    """

    kwargs = _get_kwargs(
        backup_id=backup_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    backup_id: str,
    *,
    client: AuthenticatedClient,
    body: DaemonMachineBackupRestoreResult,
) -> Optional[
    Union[
        Any,
        Error,
        ReportDaemonMachineBackupRestoreResponse4XX,
        ReportDaemonMachineBackupRestoreResponse5XX,
    ]
]:
    """Report the outcome of a pending workspace restore

    Args:
        backup_id (str):
        body (DaemonMachineBackupRestoreResult):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ReportDaemonMachineBackupRestoreResponse4XX, ReportDaemonMachineBackupRestoreResponse5XX]
    """

    return (
        await asyncio_detailed(
            backup_id=backup_id,
            client=client,
            body=body,
        )
    ).parsed
