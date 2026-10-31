from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_session_resource_response_4xx import AddSessionResourceResponse4XX
from ...models.add_session_resource_response_5xx import AddSessionResourceResponse5XX
from ...models.error import Error
from ...models.file_resource_params import FileResourceParams
from ...models.session_file_resource import SessionFileResource
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    body: FileResourceParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions/{session_id}/resources".format(
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
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
    ]
]:
    if response.status_code == 200:
        response_200 = SessionFileResource.from_dict(response.json())

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
        response_4xx = AddSessionResourceResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = AddSessionResourceResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
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
    body: FileResourceParams,
) -> Response[
    Union[
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
    ]
]:
    """Mount a file into a session

     Mounts a project file, read-only, at mount_path below /mnt/session/uploads (default
    /mnt/session/uploads/<file_id>). The mount creates a new file_id, a session instance scoped to this
    session that references the same stored content: no bytes are copied, the instance does not count
    against the storage limit, and it stays readable after the original file is deleted. The session's
    storage tools read it at mount_path. Mounting the same file at the same path again returns the
    existing resource; another file at that path is 409. Only project files can be mounted, not session
    instances (404). A session holds at most 500 files.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddSessionResourceResponse4XX, AddSessionResourceResponse5XX, Error, SessionFileResource]]
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
    body: FileResourceParams,
) -> Optional[
    Union[
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
    ]
]:
    """Mount a file into a session

     Mounts a project file, read-only, at mount_path below /mnt/session/uploads (default
    /mnt/session/uploads/<file_id>). The mount creates a new file_id, a session instance scoped to this
    session that references the same stored content: no bytes are copied, the instance does not count
    against the storage limit, and it stays readable after the original file is deleted. The session's
    storage tools read it at mount_path. Mounting the same file at the same path again returns the
    existing resource; another file at that path is 409. Only project files can be mounted, not session
    instances (404). A session holds at most 500 files.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddSessionResourceResponse4XX, AddSessionResourceResponse5XX, Error, SessionFileResource]
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
    body: FileResourceParams,
) -> Response[
    Union[
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
    ]
]:
    """Mount a file into a session

     Mounts a project file, read-only, at mount_path below /mnt/session/uploads (default
    /mnt/session/uploads/<file_id>). The mount creates a new file_id, a session instance scoped to this
    session that references the same stored content: no bytes are copied, the instance does not count
    against the storage limit, and it stays readable after the original file is deleted. The session's
    storage tools read it at mount_path. Mounting the same file at the same path again returns the
    existing resource; another file at that path is 409. Only project files can be mounted, not session
    instances (404). A session holds at most 500 files.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddSessionResourceResponse4XX, AddSessionResourceResponse5XX, Error, SessionFileResource]]
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
    body: FileResourceParams,
) -> Optional[
    Union[
        AddSessionResourceResponse4XX,
        AddSessionResourceResponse5XX,
        Error,
        SessionFileResource,
    ]
]:
    """Mount a file into a session

     Mounts a project file, read-only, at mount_path below /mnt/session/uploads (default
    /mnt/session/uploads/<file_id>). The mount creates a new file_id, a session instance scoped to this
    session that references the same stored content: no bytes are copied, the instance does not count
    against the storage limit, and it stays readable after the original file is deleted. The session's
    storage tools read it at mount_path. Mounting the same file at the same path again returns the
    existing resource; another file at that path is 409. Only project files can be mounted, not session
    instances (404). A session holds at most 500 files.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddSessionResourceResponse4XX, AddSessionResourceResponse5XX, Error, SessionFileResource]
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
