from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_terminal_session_request import CreateTerminalSessionRequest
from ...models.create_terminal_session_response_4xx import (
    CreateTerminalSessionResponse4XX,
)
from ...models.create_terminal_session_response_5xx import (
    CreateTerminalSessionResponse5XX,
)
from ...models.error import Error
from ...models.terminal_session import TerminalSession
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    machine_id: str,
    *,
    body: CreateTerminalSessionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/machines/{machine_id}/terminal-sessions".format(
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
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
    ]
]:
    if response.status_code == 201:
        response_201 = TerminalSession.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = CreateTerminalSessionResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateTerminalSessionResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
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
    body: CreateTerminalSessionRequest,
) -> Response[
    Union[
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
    ]
]:
    """Create a terminal session

     Creates a PTY-backed shell session. The PTY data plane is being wired to the machine daemon; until
    then this endpoint reports that terminal sessions are unavailable.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (CreateTerminalSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateTerminalSessionResponse4XX, CreateTerminalSessionResponse5XX, Error, TerminalSession]]
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
    body: CreateTerminalSessionRequest,
) -> Optional[
    Union[
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
    ]
]:
    """Create a terminal session

     Creates a PTY-backed shell session. The PTY data plane is being wired to the machine daemon; until
    then this endpoint reports that terminal sessions are unavailable.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (CreateTerminalSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateTerminalSessionResponse4XX, CreateTerminalSessionResponse5XX, Error, TerminalSession]
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
    body: CreateTerminalSessionRequest,
) -> Response[
    Union[
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
    ]
]:
    """Create a terminal session

     Creates a PTY-backed shell session. The PTY data plane is being wired to the machine daemon; until
    then this endpoint reports that terminal sessions are unavailable.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (CreateTerminalSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateTerminalSessionResponse4XX, CreateTerminalSessionResponse5XX, Error, TerminalSession]]
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
    body: CreateTerminalSessionRequest,
) -> Optional[
    Union[
        CreateTerminalSessionResponse4XX,
        CreateTerminalSessionResponse5XX,
        Error,
        TerminalSession,
    ]
]:
    """Create a terminal session

     Creates a PTY-backed shell session. The PTY data plane is being wired to the machine daemon; until
    then this endpoint reports that terminal sessions are unavailable.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        body (CreateTerminalSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateTerminalSessionResponse4XX, CreateTerminalSessionResponse5XX, Error, TerminalSession]
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
