from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daemon_session_output import DaemonSessionOutput
from ...models.error import Error
from ...models.upload_daemon_session_output_response_4xx import (
    UploadDaemonSessionOutputResponse4XX,
)
from ...models.upload_daemon_session_output_response_5xx import (
    UploadDaemonSessionOutputResponse5XX,
)
from ...types import UNSET, File, Response


def _get_kwargs(
    process_id: str,
    *,
    body: File,
    path: str,
    x_bma_file_digest: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-BMA-File-Digest"] = x_bma_file_digest

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/processes/{process_id}/session-outputs".format(
            process_id=process_id,
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload

    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = DaemonSessionOutput.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = DaemonSessionOutput.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if 400 <= response.status_code <= 499:
        response_4xx = UploadDaemonSessionOutputResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UploadDaemonSessionOutputResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
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
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
    x_bma_file_digest: str,
) -> Response[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
    ]
]:
    """Store a session output file

     Stores a file the agent wrote below /mnt/session/outputs as a file scoped to the process's agent
    session (listed by GET /files with scope_id). The process must be running on the calling machine or
    have ended within the last 15 minutes. Uploading the same path with the same content again returns
    the existing file (200). An output the project file storage limit cannot hold is 422.

    Args:
        process_id (str):
        path (str):
        x_bma_file_digest (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonSessionOutput, Error, UploadDaemonSessionOutputResponse4XX, UploadDaemonSessionOutputResponse5XX]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        body=body,
        path=path,
        x_bma_file_digest=x_bma_file_digest,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    process_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
    x_bma_file_digest: str,
) -> Optional[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
    ]
]:
    """Store a session output file

     Stores a file the agent wrote below /mnt/session/outputs as a file scoped to the process's agent
    session (listed by GET /files with scope_id). The process must be running on the calling machine or
    have ended within the last 15 minutes. Uploading the same path with the same content again returns
    the existing file (200). An output the project file storage limit cannot hold is 422.

    Args:
        process_id (str):
        path (str):
        x_bma_file_digest (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonSessionOutput, Error, UploadDaemonSessionOutputResponse4XX, UploadDaemonSessionOutputResponse5XX]
    """

    return sync_detailed(
        process_id=process_id,
        client=client,
        body=body,
        path=path,
        x_bma_file_digest=x_bma_file_digest,
    ).parsed


async def asyncio_detailed(
    process_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
    x_bma_file_digest: str,
) -> Response[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
    ]
]:
    """Store a session output file

     Stores a file the agent wrote below /mnt/session/outputs as a file scoped to the process's agent
    session (listed by GET /files with scope_id). The process must be running on the calling machine or
    have ended within the last 15 minutes. Uploading the same path with the same content again returns
    the existing file (200). An output the project file storage limit cannot hold is 422.

    Args:
        process_id (str):
        path (str):
        x_bma_file_digest (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonSessionOutput, Error, UploadDaemonSessionOutputResponse4XX, UploadDaemonSessionOutputResponse5XX]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        body=body,
        path=path,
        x_bma_file_digest=x_bma_file_digest,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
    x_bma_file_digest: str,
) -> Optional[
    Union[
        DaemonSessionOutput,
        Error,
        UploadDaemonSessionOutputResponse4XX,
        UploadDaemonSessionOutputResponse5XX,
    ]
]:
    """Store a session output file

     Stores a file the agent wrote below /mnt/session/outputs as a file scoped to the process's agent
    session (listed by GET /files with scope_id). The process must be running on the calling machine or
    have ended within the last 15 minutes. Uploading the same path with the same content again returns
    the existing file (200). An output the project file storage limit cannot hold is 422.

    Args:
        process_id (str):
        path (str):
        x_bma_file_digest (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonSessionOutput, Error, UploadDaemonSessionOutputResponse4XX, UploadDaemonSessionOutputResponse5XX]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            client=client,
            body=body,
            path=path,
            x_bma_file_digest=x_bma_file_digest,
        )
    ).parsed
