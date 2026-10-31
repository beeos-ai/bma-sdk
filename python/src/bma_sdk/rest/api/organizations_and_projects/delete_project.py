from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_project_response_4xx import DeleteProjectResponse4XX
from ...models.delete_project_response_5xx import DeleteProjectResponse5XX
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/orgs/{org_id}/projects/{project_id}".format(
            org_id=org_id,
            project_id=project_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
        response_4xx = DeleteProjectResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteProjectResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
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
) -> Response[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
    """Delete project

     Deletes the project, its memberships, profiles and profile versions, integrations and their
    interaction targets, project-owned skills and revisions, and grants owned by or targeting the
    project. Project-owned secrets are permanently deleted with their versions and grants. The project's
    agents are archived and their runtimes and queued work are stopped. Machine, machine-pool, and model
    grants are removed without deleting the shared machine, pool, or model. Deletion fails if agent
    teardown cannot complete.

    Args:
        org_id (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
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
) -> Optional[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
    """Delete project

     Deletes the project, its memberships, profiles and profile versions, integrations and their
    interaction targets, project-owned skills and revisions, and grants owned by or targeting the
    project. Project-owned secrets are permanently deleted with their versions and grants. The project's
    agents are archived and their runtimes and queued work are stopped. Machine, machine-pool, and model
    grants are removed without deleting the shared machine, pool, or model. Deletion fails if agent
    teardown cannot complete.

    Args:
        org_id (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
    """Delete project

     Deletes the project, its memberships, profiles and profile versions, integrations and their
    interaction targets, project-owned skills and revisions, and grants owned by or targeting the
    project. Project-owned secrets are permanently deleted with their versions and grants. The project's
    agents are archived and their runtimes and queued work are stopped. Machine, machine-pool, and model
    grants are removed without deleting the shared machine, pool, or model. Deletion fails if agent
    teardown cannot complete.

    Args:
        org_id (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]]:
    """Delete project

     Deletes the project, its memberships, profiles and profile versions, integrations and their
    interaction targets, project-owned skills and revisions, and grants owned by or targeting the
    project. Project-owned secrets are permanently deleted with their versions and grants. The project's
    agents are archived and their runtimes and queued work are stopped. Machine, machine-pool, and model
    grants are removed without deleting the shared machine, pool, or model. Deletion fails if agent
    teardown cannot complete.

    Args:
        org_id (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteProjectResponse4XX, DeleteProjectResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
        )
    ).parsed
