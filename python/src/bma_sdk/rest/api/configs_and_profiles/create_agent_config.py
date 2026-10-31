from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_config import AgentConfig
from ...models.create_agent_config_request import CreateAgentConfigRequest
from ...models.create_agent_config_response_4xx import CreateAgentConfigResponse4XX
from ...models.create_agent_config_response_5xx import CreateAgentConfigResponse5XX
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: CreateAgentConfigRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-configs".format(
            org_id=org_id,
            project_id=project_id,
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
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
    ]
]:
    if response.status_code == 200:
        response_200 = AgentConfig.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = AgentConfig.from_dict(response.json())

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
        response_4xx = CreateAgentConfigResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateAgentConfigResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
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
    *,
    client: AuthenticatedClient,
    body: CreateAgentConfigRequest,
) -> Response[
    Union[
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
    ]
]:
    """Create agent config

     Compiles and saves an immutable agent config (instruction, model, tools, machine_sources, and more)
    from YAML or JSON and returns it. Sending the same source again returns the existing config, as long
    as its names still resolve to the same resources.

    Args:
        org_id (str):
        project_id (str):
        body (CreateAgentConfigRequest): An agent config to compile. YAML sources are stored
            verbatim, so comments and formatting survive; JSON sources, as text or as an object, are
            stored canonicalized, so the same JSON definition always maps to the same config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentConfigRequest,
) -> Optional[
    Union[
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
    ]
]:
    """Create agent config

     Compiles and saves an immutable agent config (instruction, model, tools, machine_sources, and more)
    from YAML or JSON and returns it. Sending the same source again returns the existing config, as long
    as its names still resolve to the same resources.

    Args:
        org_id (str):
        project_id (str):
        body (CreateAgentConfigRequest): An agent config to compile. YAML sources are stored
            verbatim, so comments and formatting survive; JSON sources, as text or as an object, are
            stored canonicalized, so the same JSON definition always maps to the same config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentConfigRequest,
) -> Response[
    Union[
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
    ]
]:
    """Create agent config

     Compiles and saves an immutable agent config (instruction, model, tools, machine_sources, and more)
    from YAML or JSON and returns it. Sending the same source again returns the existing config, as long
    as its names still resolve to the same resources.

    Args:
        org_id (str):
        project_id (str):
        body (CreateAgentConfigRequest): An agent config to compile. YAML sources are stored
            verbatim, so comments and formatting survive; JSON sources, as text or as an object, are
            stored canonicalized, so the same JSON definition always maps to the same config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAgentConfigRequest,
) -> Optional[
    Union[
        AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error
    ]
]:
    """Create agent config

     Compiles and saves an immutable agent config (instruction, model, tools, machine_sources, and more)
    from YAML or JSON and returns it. Sending the same source again returns the existing config, as long
    as its names still resolve to the same resources.

    Args:
        org_id (str):
        project_id (str):
        body (CreateAgentConfigRequest): An agent config to compile. YAML sources are stored
            verbatim, so comments and formatting survive; JSON sources, as text or as an object, are
            stored canonicalized, so the same JSON definition always maps to the same config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConfig, CreateAgentConfigResponse4XX, CreateAgentConfigResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
