from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.desktop_agent_action_request import DesktopAgentActionRequest
from ...models.desktop_pending import DesktopPending
from ...models.error import Error
from ...models.submit_desktop_action_response_4xx import SubmitDesktopActionResponse4XX
from ...models.submit_desktop_action_response_5xx import SubmitDesktopActionResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    body: DesktopAgentActionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/machines/{machine_id}/desktop-sessions/{desktop_session_id}/agent/actions".format(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            desktop_session_id=desktop_session_id,
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
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
    ]
]:
    if response.status_code == 202:
        response_202 = DesktopPending.from_dict(response.json())

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
        response_4xx = SubmitDesktopActionResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = SubmitDesktopActionResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
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
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
    body: DesktopAgentActionRequest,
) -> Response[
    Union[
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
    ]
]:
    """Submit an agent desktop action

     Fences the action at the supplied generation and returns a pending action that must be confirmed
    after a fresh observation.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):
        body (DesktopAgentActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DesktopPending, Error, SubmitDesktopActionResponse4XX, SubmitDesktopActionResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
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
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
    body: DesktopAgentActionRequest,
) -> Optional[
    Union[
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
    ]
]:
    """Submit an agent desktop action

     Fences the action at the supplied generation and returns a pending action that must be confirmed
    after a fresh observation.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):
        body (DesktopAgentActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DesktopPending, Error, SubmitDesktopActionResponse4XX, SubmitDesktopActionResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
    body: DesktopAgentActionRequest,
) -> Response[
    Union[
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
    ]
]:
    """Submit an agent desktop action

     Fences the action at the supplied generation and returns a pending action that must be confirmed
    after a fresh observation.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):
        body (DesktopAgentActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DesktopPending, Error, SubmitDesktopActionResponse4XX, SubmitDesktopActionResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        machine_id=machine_id,
        desktop_session_id=desktop_session_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    machine_id: str,
    desktop_session_id: str,
    *,
    client: AuthenticatedClient,
    body: DesktopAgentActionRequest,
) -> Optional[
    Union[
        DesktopPending,
        Error,
        SubmitDesktopActionResponse4XX,
        SubmitDesktopActionResponse5XX,
    ]
]:
    """Submit an agent desktop action

     Fences the action at the supplied generation and returns a pending action that must be confirmed
    after a fresh observation.

    Args:
        org_id (str):
        project_id (str):
        machine_id (str):
        desktop_session_id (str):
        body (DesktopAgentActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DesktopPending, Error, SubmitDesktopActionResponse4XX, SubmitDesktopActionResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            desktop_session_id=desktop_session_id,
            client=client,
            body=body,
        )
    ).parsed
