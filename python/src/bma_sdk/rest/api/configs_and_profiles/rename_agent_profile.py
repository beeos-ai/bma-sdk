from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_profile import AgentProfile
from ...models.error import Error
from ...models.rename_agent_profile_request import RenameAgentProfileRequest
from ...models.rename_agent_profile_response_4xx import RenameAgentProfileResponse4XX
from ...models.rename_agent_profile_response_5xx import RenameAgentProfileResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    body: RenameAgentProfileRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-profiles/{agent_profile_id}".format(
            org_id=org_id,
            project_id=project_id,
            agent_profile_id=agent_profile_id,
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
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentProfile.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = RenameAgentProfileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = RenameAgentProfileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
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
    agent_profile_id: str,
    *,
    client: AuthenticatedClient,
    body: RenameAgentProfileRequest,
) -> Response[
    Union[
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
    ]
]:
    """Rename agent profile

     Renames an agent profile without changing its config. Agents and cron triggers reference the profile
    by ID and keep working, but configs that name the profile under subagents must use the new name the
    next time they're compiled.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (str):
        body (RenameAgentProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentProfile, Error, RenameAgentProfileResponse4XX, RenameAgentProfileResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: AuthenticatedClient,
    body: RenameAgentProfileRequest,
) -> Optional[
    Union[
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
    ]
]:
    """Rename agent profile

     Renames an agent profile without changing its config. Agents and cron triggers reference the profile
    by ID and keep working, but configs that name the profile under subagents must use the new name the
    next time they're compiled.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (str):
        body (RenameAgentProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentProfile, Error, RenameAgentProfileResponse4XX, RenameAgentProfileResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: AuthenticatedClient,
    body: RenameAgentProfileRequest,
) -> Response[
    Union[
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
    ]
]:
    """Rename agent profile

     Renames an agent profile without changing its config. Agents and cron triggers reference the profile
    by ID and keep working, but configs that name the profile under subagents must use the new name the
    next time they're compiled.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (str):
        body (RenameAgentProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentProfile, Error, RenameAgentProfileResponse4XX, RenameAgentProfileResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_profile_id=agent_profile_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_profile_id: str,
    *,
    client: AuthenticatedClient,
    body: RenameAgentProfileRequest,
) -> Optional[
    Union[
        AgentProfile,
        Error,
        RenameAgentProfileResponse4XX,
        RenameAgentProfileResponse5XX,
    ]
]:
    """Rename agent profile

     Renames an agent profile without changing its config. Agents and cron triggers reference the profile
    by ID and keep working, but configs that name the profile under subagents must use the new name the
    next time they're compiled.

    Args:
        org_id (str):
        project_id (str):
        agent_profile_id (str):
        body (RenameAgentProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentProfile, Error, RenameAgentProfileResponse4XX, RenameAgentProfileResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_profile_id=agent_profile_id,
            client=client,
            body=body,
        )
    ).parsed
