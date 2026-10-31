from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_config_generated_source import AgentConfigGeneratedSource
from ...models.error import Error
from ...models.get_agent_config_generated_source_response_4xx import (
    GetAgentConfigGeneratedSourceResponse4XX,
)
from ...models.get_agent_config_generated_source_response_5xx import (
    GetAgentConfigGeneratedSourceResponse5XX,
)
from ...models.get_agent_config_generated_source_source_format import (
    GetAgentConfigGeneratedSourceSourceFormat,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_config_id: str,
    *,
    source_format: Union[Unset, GetAgentConfigGeneratedSourceSourceFormat] = "yaml",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_source_format: Union[Unset, str] = UNSET
    if not isinstance(source_format, Unset):
        json_source_format = source_format

    params["source_format"] = json_source_format

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-configs/{agent_config_id}/generated-source".format(
            org_id=org_id,
            project_id=project_id,
            agent_config_id=agent_config_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = AgentConfigGeneratedSource.from_dict(response.json())

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
        response_4xx = GetAgentConfigGeneratedSourceResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetAgentConfigGeneratedSourceResponse5XX.from_dict(
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
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
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
    agent_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    source_format: Union[Unset, GetAgentConfigGeneratedSourceSourceFormat] = "yaml",
) -> Response[
    Union[
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
    ]
]:
    """Get generated agent config source

     Rebuilds a source from the config's compiled_definition, for configs saved without a source.

    Args:
        org_id (str):
        project_id (str):
        agent_config_id (str):
        source_format (Union[Unset, GetAgentConfigGeneratedSourceSourceFormat]):  Default: 'yaml'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConfigGeneratedSource, Error, GetAgentConfigGeneratedSourceResponse4XX, GetAgentConfigGeneratedSourceResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_config_id=agent_config_id,
        source_format=source_format,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    agent_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    source_format: Union[Unset, GetAgentConfigGeneratedSourceSourceFormat] = "yaml",
) -> Optional[
    Union[
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
    ]
]:
    """Get generated agent config source

     Rebuilds a source from the config's compiled_definition, for configs saved without a source.

    Args:
        org_id (str):
        project_id (str):
        agent_config_id (str):
        source_format (Union[Unset, GetAgentConfigGeneratedSourceSourceFormat]):  Default: 'yaml'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConfigGeneratedSource, Error, GetAgentConfigGeneratedSourceResponse4XX, GetAgentConfigGeneratedSourceResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_config_id=agent_config_id,
        client=client,
        source_format=source_format,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    source_format: Union[Unset, GetAgentConfigGeneratedSourceSourceFormat] = "yaml",
) -> Response[
    Union[
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
    ]
]:
    """Get generated agent config source

     Rebuilds a source from the config's compiled_definition, for configs saved without a source.

    Args:
        org_id (str):
        project_id (str):
        agent_config_id (str):
        source_format (Union[Unset, GetAgentConfigGeneratedSourceSourceFormat]):  Default: 'yaml'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConfigGeneratedSource, Error, GetAgentConfigGeneratedSourceResponse4XX, GetAgentConfigGeneratedSourceResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_config_id=agent_config_id,
        source_format=source_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    source_format: Union[Unset, GetAgentConfigGeneratedSourceSourceFormat] = "yaml",
) -> Optional[
    Union[
        AgentConfigGeneratedSource,
        Error,
        GetAgentConfigGeneratedSourceResponse4XX,
        GetAgentConfigGeneratedSourceResponse5XX,
    ]
]:
    """Get generated agent config source

     Rebuilds a source from the config's compiled_definition, for configs saved without a source.

    Args:
        org_id (str):
        project_id (str):
        agent_config_id (str):
        source_format (Union[Unset, GetAgentConfigGeneratedSourceSourceFormat]):  Default: 'yaml'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConfigGeneratedSource, Error, GetAgentConfigGeneratedSourceResponse4XX, GetAgentConfigGeneratedSourceResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_config_id=agent_config_id,
            client=client,
            source_format=source_format,
        )
    ).parsed
