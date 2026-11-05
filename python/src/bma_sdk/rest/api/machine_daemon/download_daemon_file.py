from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.download_daemon_file_response_4xx import DownloadDaemonFileResponse4XX
from ...models.download_daemon_file_response_5xx import DownloadDaemonFileResponse5XX
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    process_id: str,
    *,
    x_bma_accept_file_edit: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_accept_file_edit, Unset):
        headers["X-BMA-Accept-File-Edit"] = (
            "true" if x_bma_accept_file_edit else "false"
        )

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/daemon/processes/{process_id}/file".format(
            process_id=process_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
]:
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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = DownloadDaemonFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DownloadDaemonFileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
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
    x_bma_accept_file_edit: Union[Unset, bool] = UNSET,
) -> Response[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
]:
    """Download daemon file

     For an edit_file process the answer is the replacement (application/vnd.bma.file-edit+json) for the
    executor to apply, and only to an executor that sends X-BMA-Accept-File-Edit; any other executor
    gets a 409 and leaves the file unchanged.

    Args:
        process_id (str):
        x_bma_accept_file_edit (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        x_bma_accept_file_edit=x_bma_accept_file_edit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    process_id: str,
    *,
    client: AuthenticatedClient,
    x_bma_accept_file_edit: Union[Unset, bool] = UNSET,
) -> Optional[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
]:
    """Download daemon file

     For an edit_file process the answer is the replacement (application/vnd.bma.file-edit+json) for the
    executor to apply, and only to an executor that sends X-BMA-Accept-File-Edit; any other executor
    gets a 409 and leaves the file unchanged.

    Args:
        process_id (str):
        x_bma_accept_file_edit (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
    """

    return sync_detailed(
        process_id=process_id,
        client=client,
        x_bma_accept_file_edit=x_bma_accept_file_edit,
    ).parsed


async def asyncio_detailed(
    process_id: str,
    *,
    client: AuthenticatedClient,
    x_bma_accept_file_edit: Union[Unset, bool] = UNSET,
) -> Response[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
]:
    """Download daemon file

     For an edit_file process the answer is the replacement (application/vnd.bma.file-edit+json) for the
    executor to apply, and only to an executor that sends X-BMA-Accept-File-Edit; any other executor
    gets a 409 and leaves the file unchanged.

    Args:
        process_id (str):
        x_bma_accept_file_edit (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        x_bma_accept_file_edit=x_bma_accept_file_edit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    *,
    client: AuthenticatedClient,
    x_bma_accept_file_edit: Union[Unset, bool] = UNSET,
) -> Optional[
    Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
]:
    """Download daemon file

     For an edit_file process the answer is the replacement (application/vnd.bma.file-edit+json) for the
    executor to apply, and only to an executor that sends X-BMA-Accept-File-Edit; any other executor
    gets a 409 and leaves the file unchanged.

    Args:
        process_id (str):
        x_bma_accept_file_edit (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DownloadDaemonFileResponse4XX, DownloadDaemonFileResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            client=client,
            x_bma_accept_file_edit=x_bma_accept_file_edit,
        )
    ).parsed
