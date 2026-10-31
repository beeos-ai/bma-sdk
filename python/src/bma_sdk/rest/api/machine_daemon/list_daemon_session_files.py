from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daemon_session_files import DaemonSessionFiles
from ...models.error import Error
from ...models.list_daemon_session_files_response_4xx import (
    ListDaemonSessionFilesResponse4XX,
)
from ...models.list_daemon_session_files_response_5xx import (
    ListDaemonSessionFilesResponse5XX,
)
from ...types import Response


def _get_kwargs(
    process_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/daemon/processes/{process_id}/session-files".format(
            process_id=process_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = DaemonSessionFiles.from_dict(response.json())

        return response_200

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
        response_4xx = ListDaemonSessionFilesResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListDaemonSessionFilesResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
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
) -> Response[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
    ]
]:
    """List the session files a process sees

     Lists the files mounted into the agent session the process runs for, which the executor mirrors
    read-only below /mnt/session/uploads. The process must be starting or running on the calling
    machine.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonSessionFiles, Error, ListDaemonSessionFilesResponse4XX, ListDaemonSessionFilesResponse5XX]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    process_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
    ]
]:
    """List the session files a process sees

     Lists the files mounted into the agent session the process runs for, which the executor mirrors
    read-only below /mnt/session/uploads. The process must be starting or running on the calling
    machine.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonSessionFiles, Error, ListDaemonSessionFilesResponse4XX, ListDaemonSessionFilesResponse5XX]
    """

    return sync_detailed(
        process_id=process_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    process_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
    ]
]:
    """List the session files a process sees

     Lists the files mounted into the agent session the process runs for, which the executor mirrors
    read-only below /mnt/session/uploads. The process must be starting or running on the calling
    machine.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonSessionFiles, Error, ListDaemonSessionFilesResponse4XX, ListDaemonSessionFilesResponse5XX]]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DaemonSessionFiles,
        Error,
        ListDaemonSessionFilesResponse4XX,
        ListDaemonSessionFilesResponse5XX,
    ]
]:
    """List the session files a process sees

     Lists the files mounted into the agent session the process runs for, which the executor mirrors
    read-only below /mnt/session/uploads. The process must be starting or running on the calling
    machine.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonSessionFiles, Error, ListDaemonSessionFilesResponse4XX, ListDaemonSessionFilesResponse5XX]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            client=client,
        )
    ).parsed
