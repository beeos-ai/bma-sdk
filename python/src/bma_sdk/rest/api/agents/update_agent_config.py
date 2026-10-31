from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_agent_config_request import UpdateAgentConfigRequest
from ...models.update_agent_config_response import UpdateAgentConfigResponse
from ...models.update_agent_config_response_4xx import UpdateAgentConfigResponse4XX
from ...models.update_agent_config_response_5xx import UpdateAgentConfigResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    body: UpdateAgentConfigRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/config".format(
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
        Error,
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = UpdateAgentConfigResponse.from_dict(response.json())

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
        response_4xx = UpdateAgentConfigResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateAgentConfigResponse5XX.from_dict(response.json())

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
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
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
    body: UpdateAgentConfigRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
    ]
]:
    """Update agent config

     Replaces an active agent's config without restarting its conversation and returns the new
    agent_config. Model, instruction, and tool changes apply at the agent's next model call; machine
    changes apply immediately, stopping processes on removed machines and deleting the agent's machines
    from removed pools. Send the complete config, not a patch.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        idempotency_key (Union[Unset, str]):
        body (UpdateAgentConfigRequest): Replaces a live agent's config.
            expected_current_config_id makes the change conditional on the agent still running that
            config, so concurrent editors get a conflict instead of silently overwriting each other.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UpdateAgentConfigResponse, UpdateAgentConfigResponse4XX, UpdateAgentConfigResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        body=body,
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
    body: UpdateAgentConfigRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
    ]
]:
    """Update agent config

     Replaces an active agent's config without restarting its conversation and returns the new
    agent_config. Model, instruction, and tool changes apply at the agent's next model call; machine
    changes apply immediately, stopping processes on removed machines and deleting the agent's machines
    from removed pools. Send the complete config, not a patch.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        idempotency_key (Union[Unset, str]):
        body (UpdateAgentConfigRequest): Replaces a live agent's config.
            expected_current_config_id makes the change conditional on the agent still running that
            config, so concurrent editors get a conflict instead of silently overwriting each other.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UpdateAgentConfigResponse, UpdateAgentConfigResponse4XX, UpdateAgentConfigResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateAgentConfigRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
    ]
]:
    """Update agent config

     Replaces an active agent's config without restarting its conversation and returns the new
    agent_config. Model, instruction, and tool changes apply at the agent's next model call; machine
    changes apply immediately, stopping processes on removed machines and deleting the agent's machines
    from removed pools. Send the complete config, not a patch.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        idempotency_key (Union[Unset, str]):
        body (UpdateAgentConfigRequest): Replaces a live agent's config.
            expected_current_config_id makes the change conditional on the agent still running that
            config, so concurrent editors get a conflict instead of silently overwriting each other.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, UpdateAgentConfigResponse, UpdateAgentConfigResponse4XX, UpdateAgentConfigResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        body=body,
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
    body: UpdateAgentConfigRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        UpdateAgentConfigResponse,
        UpdateAgentConfigResponse4XX,
        UpdateAgentConfigResponse5XX,
    ]
]:
    """Update agent config

     Replaces an active agent's config without restarting its conversation and returns the new
    agent_config. Model, instruction, and tool changes apply at the agent's next model call; machine
    changes apply immediately, stopping processes on removed machines and deleting the agent's machines
    from removed pools. Send the complete config, not a patch.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        idempotency_key (Union[Unset, str]):
        body (UpdateAgentConfigRequest): Replaces a live agent's config.
            expected_current_config_id makes the change conditional on the agent still running that
            config, so concurrent editors get a conflict instead of silently overwriting each other.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, UpdateAgentConfigResponse, UpdateAgentConfigResponse4XX, UpdateAgentConfigResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
