from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_session_resource_response_4xx import (
    DeleteSessionResourceResponse4XX,
)
from ...models.delete_session_resource_response_5xx import (
    DeleteSessionResourceResponse5XX,
)
from ...models.deleted_session_resource import DeletedSessionResource
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    resource_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions/{session_id}/resources/{resource_id}".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            resource_id=resource_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
        Error,
    ]
]:
    if response.status_code == 200:
        response_200 = DeletedSessionResource.from_dict(response.json())

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
        response_4xx = DeleteSessionResourceResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteSessionResourceResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
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
    session_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
        Error,
    ]
]:
    """Unmount a file from a session

     Removes the mount and its session instance; the original file, if it still exists, is kept.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteSessionResourceResponse4XX, DeleteSessionResourceResponse5XX, DeletedSessionResource, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        resource_id=resource_id,
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
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
        Error,
    ]
]:
    """Unmount a file from a session

     Removes the mount and its session instance; the original file, if it still exists, is kept.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteSessionResourceResponse4XX, DeleteSessionResourceResponse5XX, DeletedSessionResource, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        resource_id=resource_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
        Error,
    ]
]:
    """Unmount a file from a session

     Removes the mount and its session instance; the original file, if it still exists, is kept.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteSessionResourceResponse4XX, DeleteSessionResourceResponse5XX, DeletedSessionResource, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        resource_id=resource_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DeleteSessionResourceResponse4XX,
        DeleteSessionResourceResponse5XX,
        DeletedSessionResource,
        Error,
    ]
]:
    """Unmount a file from a session

     Removes the mount and its session instance; the original file, if it still exists, is kept.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteSessionResourceResponse4XX, DeleteSessionResourceResponse5XX, DeletedSessionResource, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            resource_id=resource_id,
            client=client,
        )
    ).parsed
