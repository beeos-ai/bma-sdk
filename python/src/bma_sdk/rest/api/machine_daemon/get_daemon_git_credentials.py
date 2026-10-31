from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_daemon_git_credentials_response_4xx import (
    GetDaemonGitCredentialsResponse4XX,
)
from ...models.get_daemon_git_credentials_response_5xx import (
    GetDaemonGitCredentialsResponse5XX,
)
from ...models.get_daemon_git_credentials_response_200 import (
    GetDaemonGitCredentialsResponse200,
)
from ...types import Response


def _get_kwargs(
    process_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/processes/{process_id}/git-credentials".format(
            process_id=process_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = GetDaemonGitCredentialsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
        response_4xx = GetDaemonGitCredentialsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetDaemonGitCredentialsResponse5XX.from_dict(response.json())

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
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
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
        Error,
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
    ]
]:
    """Get Git credentials for an active daemon process

     Requires machine daemon authentication and an active, execution-granted process on that machine. The
    process's original config and the agent's current config must have the same Git credentials
    settings. Credentials are limited to those settings' repositories and permission and are
    reauthorized on every request.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetDaemonGitCredentialsResponse200, GetDaemonGitCredentialsResponse4XX, GetDaemonGitCredentialsResponse5XX]]
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
        Error,
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
    ]
]:
    """Get Git credentials for an active daemon process

     Requires machine daemon authentication and an active, execution-granted process on that machine. The
    process's original config and the agent's current config must have the same Git credentials
    settings. Credentials are limited to those settings' repositories and permission and are
    reauthorized on every request.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetDaemonGitCredentialsResponse200, GetDaemonGitCredentialsResponse4XX, GetDaemonGitCredentialsResponse5XX]
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
        Error,
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
    ]
]:
    """Get Git credentials for an active daemon process

     Requires machine daemon authentication and an active, execution-granted process on that machine. The
    process's original config and the agent's current config must have the same Git credentials
    settings. Credentials are limited to those settings' repositories and permission and are
    reauthorized on every request.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetDaemonGitCredentialsResponse200, GetDaemonGitCredentialsResponse4XX, GetDaemonGitCredentialsResponse5XX]]
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
        Error,
        GetDaemonGitCredentialsResponse200,
        GetDaemonGitCredentialsResponse4XX,
        GetDaemonGitCredentialsResponse5XX,
    ]
]:
    """Get Git credentials for an active daemon process

     Requires machine daemon authentication and an active, execution-granted process on that machine. The
    process's original config and the agent's current config must have the same Git credentials
    settings. Credentials are limited to those settings' repositories and permission and are
    reauthorized on every request.

    Args:
        process_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetDaemonGitCredentialsResponse200, GetDaemonGitCredentialsResponse4XX, GetDaemonGitCredentialsResponse5XX]
    """

    return (
        await asyncio_detailed(
            process_id=process_id,
            client=client,
        )
    ).parsed
