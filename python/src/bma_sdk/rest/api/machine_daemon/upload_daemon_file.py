from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.upload_daemon_file_response_4xx import UploadDaemonFileResponse4XX
from ...models.upload_daemon_file_response_5xx import UploadDaemonFileResponse5XX
from ...models.upload_file_response import UploadFileResponse
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    process_id: str,
    *,
    body: File,
    filename: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["filename"] = filename

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/processes/{process_id}/file".format(
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
        Error,
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
    ]
]:
    if response.status_code == 201:
        response_201 = UploadFileResponse.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = UploadDaemonFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UploadDaemonFileResponse5XX.from_dict(response.json())

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
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
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
    filename: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
    ]
]:
    """Upload daemon file

    Args:
        process_id (str):
        filename (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadDaemonFileResponse4XX, UploadDaemonFileResponse5XX, UploadFileResponse]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        body=body,
        filename=filename,
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
    filename: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
    ]
]:
    """Upload daemon file

    Args:
        process_id (str):
        filename (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadDaemonFileResponse4XX, UploadDaemonFileResponse5XX, UploadFileResponse]
    """

    return sync_detailed(
        process_id=process_id,
        client=client,
        body=body,
        filename=filename,
    ).parsed


async def asyncio_detailed(
    process_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    filename: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
    ]
]:
    """Upload daemon file

    Args:
        process_id (str):
        filename (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UploadDaemonFileResponse4XX, UploadDaemonFileResponse5XX, UploadFileResponse]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        body=body,
        filename=filename,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    filename: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        UploadDaemonFileResponse4XX,
        UploadDaemonFileResponse5XX,
        UploadFileResponse,
    ]
]:
    """Upload daemon file

    Args:
        process_id (str):
        filename (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UploadDaemonFileResponse4XX, UploadDaemonFileResponse5XX, UploadFileResponse]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            client=client,
            body=body,
            filename=filename,
        )
    ).parsed
