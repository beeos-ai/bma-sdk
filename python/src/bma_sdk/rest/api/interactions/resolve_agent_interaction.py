from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_interaction import AgentInteraction
from ...models.error import Error
from ...models.resolve_agent_interaction_request import ResolveAgentInteractionRequest
from ...models.resolve_agent_interaction_response_4xx import (
    ResolveAgentInteractionResponse4XX,
)
from ...models.resolve_agent_interaction_response_5xx import (
    ResolveAgentInteractionResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    interaction_id: str,
    *,
    body: ResolveAgentInteractionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/interactions/{interaction_id}/resolve".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            interaction_id=interaction_id,
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
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentInteraction.from_dict(response.json())

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
        response_4xx = ResolveAgentInteractionResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ResolveAgentInteractionResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
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
    agent_id: str,
    interaction_id: str,
    *,
    client: AuthenticatedClient,
    body: ResolveAgentInteractionRequest,
) -> Response[
    Union[
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
    ]
]:
    """Resolve agent interaction

     Answers an open permission prompt or question so the paused agent resumes, and returns the resolved
    interaction. Send one answer per question with zero-based option_indices; permission prompts use 0
    for Allow and 1 for Deny.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        interaction_id (str):
        body (ResolveAgentInteractionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentInteraction, Error, ResolveAgentInteractionResponse4XX, ResolveAgentInteractionResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        interaction_id=interaction_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_id: str,
    interaction_id: str,
    *,
    client: AuthenticatedClient,
    body: ResolveAgentInteractionRequest,
) -> Optional[
    Union[
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
    ]
]:
    """Resolve agent interaction

     Answers an open permission prompt or question so the paused agent resumes, and returns the resolved
    interaction. Send one answer per question with zero-based option_indices; permission prompts use 0
    for Allow and 1 for Deny.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        interaction_id (str):
        body (ResolveAgentInteractionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentInteraction, Error, ResolveAgentInteractionResponse4XX, ResolveAgentInteractionResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        interaction_id=interaction_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    interaction_id: str,
    *,
    client: AuthenticatedClient,
    body: ResolveAgentInteractionRequest,
) -> Response[
    Union[
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
    ]
]:
    """Resolve agent interaction

     Answers an open permission prompt or question so the paused agent resumes, and returns the resolved
    interaction. Send one answer per question with zero-based option_indices; permission prompts use 0
    for Allow and 1 for Deny.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        interaction_id (str):
        body (ResolveAgentInteractionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentInteraction, Error, ResolveAgentInteractionResponse4XX, ResolveAgentInteractionResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        interaction_id=interaction_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    interaction_id: str,
    *,
    client: AuthenticatedClient,
    body: ResolveAgentInteractionRequest,
) -> Optional[
    Union[
        AgentInteraction,
        Error,
        ResolveAgentInteractionResponse4XX,
        ResolveAgentInteractionResponse5XX,
    ]
]:
    """Resolve agent interaction

     Answers an open permission prompt or question so the paused agent resumes, and returns the resolved
    interaction. Send one answer per question with zero-based option_indices; permission prompts use 0
    for Allow and 1 for Deny.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        interaction_id (str):
        body (ResolveAgentInteractionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentInteraction, Error, ResolveAgentInteractionResponse4XX, ResolveAgentInteractionResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            interaction_id=interaction_id,
            client=client,
            body=body,
        )
    ).parsed
