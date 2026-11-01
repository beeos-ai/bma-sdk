from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_executor_binding_envelope import AgentExecutorBindingEnvelope
from ...models.agent_executor_binding_input import AgentExecutorBindingInput
from ...models.error import Error
from ...models.put_agent_executor_binding_response_4xx import (
    PutAgentExecutorBindingResponse4XX,
)
from ...models.put_agent_executor_binding_response_5xx import (
    PutAgentExecutorBindingResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    body: AgentExecutorBindingInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/executor-binding".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
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
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentExecutorBindingEnvelope.from_dict(response.json())

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

    if 400 <= response.status_code <= 499:
        response_4xx = PutAgentExecutorBindingResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = PutAgentExecutorBindingResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
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
    body: AgentExecutorBindingInput,
) -> Response[
    Union[
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
    ]
]:
    """Run the agent on an agent executor

     Binds the agent to a machine whose executor runs a complete local agent (Executor Protocol
    capability agent). Session input then becomes turn.start / turn.input on that executor, session
    cancel turn.cancel and session archive session.close; the BMA harness does not run the agent's
    sessions. Input queues while the executor is offline.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (AgentExecutorBindingInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentExecutorBindingEnvelope, Error, PutAgentExecutorBindingResponse4XX, PutAgentExecutorBindingResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
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
    *,
    client: AuthenticatedClient,
    body: AgentExecutorBindingInput,
) -> Optional[
    Union[
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
    ]
]:
    """Run the agent on an agent executor

     Binds the agent to a machine whose executor runs a complete local agent (Executor Protocol
    capability agent). Session input then becomes turn.start / turn.input on that executor, session
    cancel turn.cancel and session archive session.close; the BMA harness does not run the agent's
    sessions. Input queues while the executor is offline.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (AgentExecutorBindingInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentExecutorBindingEnvelope, Error, PutAgentExecutorBindingResponse4XX, PutAgentExecutorBindingResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentExecutorBindingInput,
) -> Response[
    Union[
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
    ]
]:
    """Run the agent on an agent executor

     Binds the agent to a machine whose executor runs a complete local agent (Executor Protocol
    capability agent). Session input then becomes turn.start / turn.input on that executor, session
    cancel turn.cancel and session archive session.close; the BMA harness does not run the agent's
    sessions. Input queues while the executor is offline.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (AgentExecutorBindingInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentExecutorBindingEnvelope, Error, PutAgentExecutorBindingResponse4XX, PutAgentExecutorBindingResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentExecutorBindingInput,
) -> Optional[
    Union[
        AgentExecutorBindingEnvelope,
        Error,
        PutAgentExecutorBindingResponse4XX,
        PutAgentExecutorBindingResponse5XX,
    ]
]:
    """Run the agent on an agent executor

     Binds the agent to a machine whose executor runs a complete local agent (Executor Protocol
    capability agent). Session input then becomes turn.start / turn.input on that executor, session
    cancel turn.cancel and session archive session.close; the BMA harness does not run the agent's
    sessions. Input queues while the executor is offline.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (AgentExecutorBindingInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentExecutorBindingEnvelope, Error, PutAgentExecutorBindingResponse4XX, PutAgentExecutorBindingResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            body=body,
        )
    ).parsed
