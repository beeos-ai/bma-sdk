from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project_file import ProjectFile
from ...models.promote_session_artifact_request import PromoteSessionArtifactRequest
from ...models.promote_session_artifact_response_4xx import (
    PromoteSessionArtifactResponse4XX,
)
from ...models.promote_session_artifact_response_5xx import (
    PromoteSessionArtifactResponse5XX,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    artifact_id: str,
    *,
    body: PromoteSessionArtifactRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/sessions/{session_id}/artifacts/{artifact_id}/promote".format(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            artifact_id=artifact_id,
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
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ProjectFile.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = ProjectFile.from_dict(response.json())

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
        response_4xx = PromoteSessionArtifactResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = PromoteSessionArtifactResponse5XX.from_dict(response.json())

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
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
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
    artifact_id: str,
    *,
    client: AuthenticatedClient,
    body: PromoteSessionArtifactRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
    ]
]:
    r"""Promote a session artifact to a file

     Copies an artifact this session owns into a project file inside BMA, without the caller downloading
    it. The file is project-wide, or scoped to the session with scope \"session\" (listed by scope_id).
    The artifact is kept. An Idempotency-Key replay returns the original file with 200.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        artifact_id (str):
        idempotency_key (Union[Unset, str]):
        body (PromoteSessionArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectFile, PromoteSessionArtifactResponse4XX, PromoteSessionArtifactResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        artifact_id=artifact_id,
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
    session_id: str,
    artifact_id: str,
    *,
    client: AuthenticatedClient,
    body: PromoteSessionArtifactRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
    ]
]:
    r"""Promote a session artifact to a file

     Copies an artifact this session owns into a project file inside BMA, without the caller downloading
    it. The file is project-wide, or scoped to the session with scope \"session\" (listed by scope_id).
    The artifact is kept. An Idempotency-Key replay returns the original file with 200.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        artifact_id (str):
        idempotency_key (Union[Unset, str]):
        body (PromoteSessionArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectFile, PromoteSessionArtifactResponse4XX, PromoteSessionArtifactResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        artifact_id=artifact_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    artifact_id: str,
    *,
    client: AuthenticatedClient,
    body: PromoteSessionArtifactRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
    ]
]:
    r"""Promote a session artifact to a file

     Copies an artifact this session owns into a project file inside BMA, without the caller downloading
    it. The file is project-wide, or scoped to the session with scope \"session\" (listed by scope_id).
    The artifact is kept. An Idempotency-Key replay returns the original file with 200.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        artifact_id (str):
        idempotency_key (Union[Unset, str]):
        body (PromoteSessionArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectFile, PromoteSessionArtifactResponse4XX, PromoteSessionArtifactResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        agent_id=agent_id,
        session_id=session_id,
        artifact_id=artifact_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    agent_id: str,
    session_id: str,
    artifact_id: str,
    *,
    client: AuthenticatedClient,
    body: PromoteSessionArtifactRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ProjectFile,
        PromoteSessionArtifactResponse4XX,
        PromoteSessionArtifactResponse5XX,
    ]
]:
    r"""Promote a session artifact to a file

     Copies an artifact this session owns into a project file inside BMA, without the caller downloading
    it. The file is project-wide, or scoped to the session with scope \"session\" (listed by scope_id).
    The artifact is kept. An Idempotency-Key replay returns the original file with 200.

    Args:
        org_id (str):
        project_id (str):
        agent_id (str):
        session_id (str):
        artifact_id (str):
        idempotency_key (Union[Unset, str]):
        body (PromoteSessionArtifactRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectFile, PromoteSessionArtifactResponse4XX, PromoteSessionArtifactResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            session_id=session_id,
            artifact_id=artifact_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
