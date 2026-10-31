from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.machine_backup import MachineBackup
from ...models.restore_machine_from_backup_request import (
    RestoreMachineFromBackupRequest,
)
from ...models.restore_machine_from_backup_response_4xx import (
    RestoreMachineFromBackupResponse4XX,
)
from ...models.restore_machine_from_backup_response_5xx import (
    RestoreMachineFromBackupResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    machine_id: str,
    *,
    body: RestoreMachineFromBackupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/machines/{machine_id}/restore".format(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
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
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
    ]
]:
    if response.status_code == 202:
        response_202 = MachineBackup.from_dict(response.json())

        return response_202

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
        response_4xx = RestoreMachineFromBackupResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = RestoreMachineFromBackupResponse5XX.from_dict(response.json())

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
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
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
    *,
    client: AuthenticatedClient,
    body: RestoreMachineFromBackupRequest,
) -> Response[
    Union[
        Error,
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
    ]
]:
    """Recreate a machine from a workspace backup

     Replaces the machine with a new one created from its template and restores a backup (the newest
    ready one unless backup_id is given) before the machine comes online again. Only files under the
    backed-up paths are restored; system-level changes and running processes are not kept. The machine's
    lifecycle_reason_code reports restoring_from_backup, then restored_from_backup or
    backup_restore_failed. BMA does the same on its own when the provider loses a machine that has a
    backup.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (RestoreMachineFromBackupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MachineBackup, RestoreMachineFromBackupResponse4XX, RestoreMachineFromBackupResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    machine_id: str,
    *,
    client: AuthenticatedClient,
    body: RestoreMachineFromBackupRequest,
) -> Optional[
    Union[
        Error,
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
    ]
]:
    """Recreate a machine from a workspace backup

     Replaces the machine with a new one created from its template and restores a backup (the newest
    ready one unless backup_id is given) before the machine comes online again. Only files under the
    backed-up paths are restored; system-level changes and running processes are not kept. The machine's
    lifecycle_reason_code reports restoring_from_backup, then restored_from_backup or
    backup_restore_failed. BMA does the same on its own when the provider loses a machine that has a
    backup.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (RestoreMachineFromBackupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MachineBackup, RestoreMachineFromBackupResponse4XX, RestoreMachineFromBackupResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    machine_id: str,
    *,
    client: AuthenticatedClient,
    body: RestoreMachineFromBackupRequest,
) -> Response[
    Union[
        Error,
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
    ]
]:
    """Recreate a machine from a workspace backup

     Replaces the machine with a new one created from its template and restores a backup (the newest
    ready one unless backup_id is given) before the machine comes online again. Only files under the
    backed-up paths are restored; system-level changes and running processes are not kept. The machine's
    lifecycle_reason_code reports restoring_from_backup, then restored_from_backup or
    backup_restore_failed. BMA does the same on its own when the provider loses a machine that has a
    backup.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (RestoreMachineFromBackupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MachineBackup, RestoreMachineFromBackupResponse4XX, RestoreMachineFromBackupResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    machine_id: str,
    *,
    client: AuthenticatedClient,
    body: RestoreMachineFromBackupRequest,
) -> Optional[
    Union[
        Error,
        MachineBackup,
        RestoreMachineFromBackupResponse4XX,
        RestoreMachineFromBackupResponse5XX,
    ]
]:
    """Recreate a machine from a workspace backup

     Replaces the machine with a new one created from its template and restores a backup (the newest
    ready one unless backup_id is given) before the machine comes online again. Only files under the
    backed-up paths are restored; system-level changes and running processes are not kept. The machine's
    lifecycle_reason_code reports restoring_from_backup, then restored_from_backup or
    backup_restore_failed. BMA does the same on its own when the provider loses a machine that has a
    backup.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (RestoreMachineFromBackupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MachineBackup, RestoreMachineFromBackupResponse4XX, RestoreMachineFromBackupResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            client=client,
            body=body,
        )
    ).parsed
