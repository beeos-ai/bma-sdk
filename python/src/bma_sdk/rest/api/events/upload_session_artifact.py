from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact import Artifact
from ...models.error import Error
from ...models.upload_session_artifact_response_4xx import (
    UploadSessionArtifactResponse4XX,
)
from ...models.upload_session_artifact_response_5xx import (
    UploadSessionArtifactResponse5XX,
)
from ...types import UNSET, File, Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    body: File,
    filename: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["filename"] = filename

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions/{session_id}/artifacts".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload

    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
    ]
]:
    if response.status_code == 201:
        response_201 = Artifact.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = UploadSessionArtifactResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UploadSessionArtifactResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
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
    body: File,
    filename: str,
) -> Response[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
    ]
]:
    """Upload a session artifact

     Streams the request body (1 byte to 1 GiB) into object storage as an artifact owned by this session.
    The session's tool calls read it at the returned /artifacts/<id> path; other sessions cannot.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        filename (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Artifact, Error, UploadSessionArtifactResponse4XX, UploadSessionArtifactResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        body=body,
        filename=filename,
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
    body: File,
    filename: str,
) -> Optional[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
    ]
]:
    """Upload a session artifact

     Streams the request body (1 byte to 1 GiB) into object storage as an artifact owned by this session.
    The session's tool calls read it at the returned /artifacts/<id> path; other sessions cannot.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        filename (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Artifact, Error, UploadSessionArtifactResponse4XX, UploadSessionArtifactResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        client=client,
        body=body,
        filename=filename,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    filename: str,
) -> Response[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
    ]
]:
    """Upload a session artifact

     Streams the request body (1 byte to 1 GiB) into object storage as an artifact owned by this session.
    The session's tool calls read it at the returned /artifacts/<id> path; other sessions cannot.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        filename (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Artifact, Error, UploadSessionArtifactResponse4XX, UploadSessionArtifactResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        body=body,
        filename=filename,
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
    body: File,
    filename: str,
) -> Optional[
    Union[
        Artifact,
        Error,
        UploadSessionArtifactResponse4XX,
        UploadSessionArtifactResponse5XX,
    ]
]:
    """Upload a session artifact

     Streams the request body (1 byte to 1 GiB) into object storage as an artifact owned by this session.
    The session's tool calls read it at the returned /artifacts/<id> path; other sessions cannot.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        filename (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Artifact, Error, UploadSessionArtifactResponse4XX, UploadSessionArtifactResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            client=client,
            body=body,
            filename=filename,
        )
    ).parsed
