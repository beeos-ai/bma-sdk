from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_model_override_envelope import AgentModelOverrideEnvelope
from ...models.agent_model_override_input import AgentModelOverrideInput
from ...models.error import Error
from ...models.put_agent_session_model_override_response_4xx import (
    PutAgentSessionModelOverrideResponse4XX,
)
from ...models.put_agent_session_model_override_response_5xx import (
    PutAgentSessionModelOverrideResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    body: AgentModelOverrideInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions/{session_id}/model-override".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
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
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentModelOverrideEnvelope.from_dict(response.json())

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

    if 400 <= response.status_code <= 499:
        response_4xx = PutAgentSessionModelOverrideResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = PutAgentSessionModelOverrideResponse5XX.from_dict(
            response.json()
        )

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
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
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentModelOverrideInput,
) -> Response[
    Union[
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
    ]
]:
    """Create or replace a session model override

     Materializes an ephemeral tenant secret, provider config, configured model and project grant for
    this session's next model call. The pinned session config revision is never modified. The response
    contains only override metadata and a fingerprint/key hint; the API key is write-only and encrypted
    at rest.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (AgentModelOverrideInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentModelOverrideEnvelope, Error, PutAgentSessionModelOverrideResponse4XX, PutAgentSessionModelOverrideResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
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
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentModelOverrideInput,
) -> Optional[
    Union[
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
    ]
]:
    """Create or replace a session model override

     Materializes an ephemeral tenant secret, provider config, configured model and project grant for
    this session's next model call. The pinned session config revision is never modified. The response
    contains only override metadata and a fingerprint/key hint; the API key is write-only and encrypted
    at rest.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (AgentModelOverrideInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentModelOverrideEnvelope, Error, PutAgentSessionModelOverrideResponse4XX, PutAgentSessionModelOverrideResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentModelOverrideInput,
) -> Response[
    Union[
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
    ]
]:
    """Create or replace a session model override

     Materializes an ephemeral tenant secret, provider config, configured model and project grant for
    this session's next model call. The pinned session config revision is never modified. The response
    contains only override metadata and a fingerprint/key hint; the API key is write-only and encrypted
    at rest.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (AgentModelOverrideInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentModelOverrideEnvelope, Error, PutAgentSessionModelOverrideResponse4XX, PutAgentSessionModelOverrideResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentModelOverrideInput,
) -> Optional[
    Union[
        AgentModelOverrideEnvelope,
        Error,
        PutAgentSessionModelOverrideResponse4XX,
        PutAgentSessionModelOverrideResponse5XX,
    ]
]:
    """Create or replace a session model override

     Materializes an ephemeral tenant secret, provider config, configured model and project grant for
    this session's next model call. The pinned session config revision is never modified. The response
    contains only override metadata and a fingerprint/key hint; the API key is write-only and encrypted
    at rest.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (AgentModelOverrideInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentModelOverrideEnvelope, Error, PutAgentSessionModelOverrideResponse4XX, PutAgentSessionModelOverrideResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            client=client,
            body=body,
        )
    ).parsed
