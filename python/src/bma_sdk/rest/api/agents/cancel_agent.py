from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_agent_request import CancelAgentRequest
from ...models.cancel_agent_response import CancelAgentResponse
from ...models.cancel_agent_response_4xx import CancelAgentResponse4XX
from ...models.cancel_agent_response_5xx import CancelAgentResponse5XX
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    body: CancelAgentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/cancel".format(
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
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
]:
    if response.status_code == 200:
        response_200 = CancelAgentResponse.from_dict(response.json())

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
        response_4xx = CancelAgentResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CancelAgentResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
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
    body: CancelAgentRequest,
) -> Response[
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
]:
    """Cancel agent

     Stops the agent's current turn: cancels its unfinished tool calls and open interactions, stops
    processes whose run_command hasn't returned yet, and discards pending steering messages. The agent
    stays active and keeps its queued messages, and processes whose run_command already returned keep
    running. Returns affected false and changes nothing when no turn is in progress. With per-session
    concurrent claims the current turn of every session is stopped; use cancelAgentSession to stop one
    session only. An archived agent cannot be canceled: the request fails with
    `state_transition_conflict`, matching input to an archived session.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (CancelAgentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]]
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
    body: CancelAgentRequest,
) -> Optional[
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
]:
    """Cancel agent

     Stops the agent's current turn: cancels its unfinished tool calls and open interactions, stops
    processes whose run_command hasn't returned yet, and discards pending steering messages. The agent
    stays active and keeps its queued messages, and processes whose run_command already returned keep
    running. Returns affected false and changes nothing when no turn is in progress. With per-session
    concurrent claims the current turn of every session is stopped; use cancelAgentSession to stop one
    session only. An archived agent cannot be canceled: the request fails with
    `state_transition_conflict`, matching input to an archived session.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (CancelAgentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
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
    body: CancelAgentRequest,
) -> Response[
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
]:
    """Cancel agent

     Stops the agent's current turn: cancels its unfinished tool calls and open interactions, stops
    processes whose run_command hasn't returned yet, and discards pending steering messages. The agent
    stays active and keeps its queued messages, and processes whose run_command already returned keep
    running. Returns affected false and changes nothing when no turn is in progress. With per-session
    concurrent claims the current turn of every session is stopped; use cancelAgentSession to stop one
    session only. An archived agent cannot be canceled: the request fails with
    `state_transition_conflict`, matching input to an archived session.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (CancelAgentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]]
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
    body: CancelAgentRequest,
) -> Optional[
    Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
]:
    """Cancel agent

     Stops the agent's current turn: cancels its unfinished tool calls and open interactions, stops
    processes whose run_command hasn't returned yet, and discards pending steering messages. The agent
    stays active and keeps its queued messages, and processes whose run_command already returned keep
    running. Returns affected false and changes nothing when no turn is in progress. With per-session
    concurrent claims the current turn of every session is stopped; use cancelAgentSession to stop one
    session only. An archived agent cannot be canceled: the request fails with
    `state_transition_conflict`, matching input to an archived session.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        body (CancelAgentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CancelAgentResponse, CancelAgentResponse4XX, CancelAgentResponse5XX, Error]
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
