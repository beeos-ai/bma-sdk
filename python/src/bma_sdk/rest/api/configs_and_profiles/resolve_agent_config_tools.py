from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.resolve_agent_config_tools_request import ResolveAgentConfigToolsRequest
from ...models.resolve_agent_config_tools_response_4xx import (
    ResolveAgentConfigToolsResponse4XX,
)
from ...models.resolved_agent_config_tools import ResolvedAgentConfigTools
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: ResolveAgentConfigToolsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agent-configs/tools".format(
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
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
]:
    if response.status_code == 200:
        response_200 = ResolvedAgentConfigTools.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ResolveAgentConfigToolsResponse4XX.from_dict(response.json())

        return response_4xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
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
    body: ResolveAgentConfigToolsRequest,
) -> Response[
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
]:
    """Resolve agent config tools

     Returns configured built-in and custom tools plus missing machine, skill, subagent, and retrieval
    defaults, including disabled entries. Accepts YAML/JSON source. Source previews validate tool-
    related fields only; they do not validate whether the config can be saved or launched. Does not
    resolve contextual integration tools, discover MCP tools, or change any configuration.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (ResolveAgentConfigToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]]
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
    body: ResolveAgentConfigToolsRequest,
) -> Optional[
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
]:
    """Resolve agent config tools

     Returns configured built-in and custom tools plus missing machine, skill, subagent, and retrieval
    defaults, including disabled entries. Accepts YAML/JSON source. Source previews validate tool-
    related fields only; they do not validate whether the config can be saved or launched. Does not
    resolve contextual integration tools, discover MCP tools, or change any configuration.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (ResolveAgentConfigToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
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
    body: ResolveAgentConfigToolsRequest,
) -> Response[
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
]:
    """Resolve agent config tools

     Returns configured built-in and custom tools plus missing machine, skill, subagent, and retrieval
    defaults, including disabled entries. Accepts YAML/JSON source. Source previews validate tool-
    related fields only; they do not validate whether the config can be saved or launched. Does not
    resolve contextual integration tools, discover MCP tools, or change any configuration.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (ResolveAgentConfigToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]]
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
    body: ResolveAgentConfigToolsRequest,
) -> Optional[
    Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
]:
    """Resolve agent config tools

     Returns configured built-in and custom tools plus missing machine, skill, subagent, and retrieval
    defaults, including disabled entries. Accepts YAML/JSON source. Source previews validate tool-
    related fields only; they do not validate whether the config can be saved or launched. Does not
    resolve contextual integration tools, discover MCP tools, or change any configuration.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        body (ResolveAgentConfigToolsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ResolveAgentConfigToolsResponse4XX, ResolvedAgentConfigTools]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
