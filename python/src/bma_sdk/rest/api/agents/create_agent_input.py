from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_input_envelope import AgentInputEnvelope
from ...models.create_agent_input_request import CreateAgentInputRequest
from ...models.create_agent_input_response_4xx import CreateAgentInputResponse4XX
from ...models.create_agent_input_response_5xx import CreateAgentInputResponse5XX
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    body: CreateAgentInputRequest,
    session_id: Union[Unset, str] = UNSET,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    params["session_id"] = session_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/inputs".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentInputEnvelope.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = AgentInputEnvelope.from_dict(response.json())

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
        response_4xx = CreateAgentInputResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateAgentInputResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
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
    *,
    client: AuthenticatedClient,
    body: CreateAgentInputRequest,
    session_id: Union[Unset, str] = UNSET,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
    ]
]:
    """Create agent input

     Sends a message to an agent and returns the stored input. Queued messages (the default) wait until
    the agent is ready for new work; steering messages reach it at its next model call.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        idempotency_key (Union[Unset, str]):
        body (CreateAgentInputRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentInputEnvelope, CreateAgentInputResponse4XX, CreateAgentInputResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        body=body,
        session_id=session_id,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentInputRequest,
    session_id: Union[Unset, str] = UNSET,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
    ]
]:
    """Create agent input

     Sends a message to an agent and returns the stored input. Queued messages (the default) wait until
    the agent is ready for new work; steering messages reach it at its next model call.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        idempotency_key (Union[Unset, str]):
        body (CreateAgentInputRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentInputEnvelope, CreateAgentInputResponse4XX, CreateAgentInputResponse5XX, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        body=body,
        session_id=session_id,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentInputRequest,
    session_id: Union[Unset, str] = UNSET,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
    ]
]:
    """Create agent input

     Sends a message to an agent and returns the stored input. Queued messages (the default) wait until
    the agent is ready for new work; steering messages reach it at its next model call.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        idempotency_key (Union[Unset, str]):
        body (CreateAgentInputRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentInputEnvelope, CreateAgentInputResponse4XX, CreateAgentInputResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        body=body,
        session_id=session_id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentInputRequest,
    session_id: Union[Unset, str] = UNSET,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        AgentInputEnvelope,
        CreateAgentInputResponse4XX,
        CreateAgentInputResponse5XX,
        Error,
    ]
]:
    """Create agent input

     Sends a message to an agent and returns the stored input. Queued messages (the default) wait until
    the agent is ready for new work; steering messages reach it at its next model call.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (Union[Unset, str]):
        idempotency_key (Union[Unset, str]):
        body (CreateAgentInputRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentInputEnvelope, CreateAgentInputResponse4XX, CreateAgentInputResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            body=body,
            session_id=session_id,
            idempotency_key=idempotency_key,
        )
    ).parsed
