from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.submit_tool_call_result_request import SubmitToolCallResultRequest
from ...models.submit_tool_call_result_response import SubmitToolCallResultResponse
from ...models.submit_tool_call_result_response_4xx import (
    SubmitToolCallResultResponse4XX,
)
from ...models.submit_tool_call_result_response_5xx import (
    SubmitToolCallResultResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    tool_call_id: str,
    *,
    body: SubmitToolCallResultRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/tool-calls/{tool_call_id}/result".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            tool_call_id=tool_call_id,
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
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
    ]
]:
    if response.status_code == 201:
        response_201 = SubmitToolCallResultResponse.from_dict(response.json())

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
        response_4xx = SubmitToolCallResultResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = SubmitToolCallResultResponse5XX.from_dict(response.json())

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
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
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
    tool_call_id: str,
    *,
    client: AuthenticatedClient,
    body: SubmitToolCallResultRequest,
) -> Response[
    Union[
        Error,
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
    ]
]:
    """Submit a result for a ready custom tool call

     Only ready custom tool calls accept externally supplied results. The first accepted result completes
    the call. Any later submission, or a result for a non-custom tool call, returns 409.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        tool_call_id (str):
        body (SubmitToolCallResultRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SubmitToolCallResultResponse, SubmitToolCallResultResponse4XX, SubmitToolCallResultResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        tool_call_id=tool_call_id,
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
    tool_call_id: str,
    *,
    client: AuthenticatedClient,
    body: SubmitToolCallResultRequest,
) -> Optional[
    Union[
        Error,
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
    ]
]:
    """Submit a result for a ready custom tool call

     Only ready custom tool calls accept externally supplied results. The first accepted result completes
    the call. Any later submission, or a result for a non-custom tool call, returns 409.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        tool_call_id (str):
        body (SubmitToolCallResultRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SubmitToolCallResultResponse, SubmitToolCallResultResponse4XX, SubmitToolCallResultResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        tool_call_id=tool_call_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    tool_call_id: str,
    *,
    client: AuthenticatedClient,
    body: SubmitToolCallResultRequest,
) -> Response[
    Union[
        Error,
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
    ]
]:
    """Submit a result for a ready custom tool call

     Only ready custom tool calls accept externally supplied results. The first accepted result completes
    the call. Any later submission, or a result for a non-custom tool call, returns 409.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        tool_call_id (str):
        body (SubmitToolCallResultRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SubmitToolCallResultResponse, SubmitToolCallResultResponse4XX, SubmitToolCallResultResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        tool_call_id=tool_call_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    tool_call_id: str,
    *,
    client: AuthenticatedClient,
    body: SubmitToolCallResultRequest,
) -> Optional[
    Union[
        Error,
        SubmitToolCallResultResponse,
        SubmitToolCallResultResponse4XX,
        SubmitToolCallResultResponse5XX,
    ]
]:
    """Submit a result for a ready custom tool call

     Only ready custom tool calls accept externally supplied results. The first accepted result completes
    the call. Any later submission, or a result for a non-custom tool call, returns 409.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        tool_call_id (str):
        body (SubmitToolCallResultRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SubmitToolCallResultResponse, SubmitToolCallResultResponse4XX, SubmitToolCallResultResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            tool_call_id=tool_call_id,
            client=client,
            body=body,
        )
    ).parsed
