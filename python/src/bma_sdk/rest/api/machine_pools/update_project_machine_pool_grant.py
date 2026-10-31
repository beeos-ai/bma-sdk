from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project_machine_pool_grant import ProjectMachinePoolGrant
from ...models.update_project_machine_pool_grant_request import (
    UpdateProjectMachinePoolGrantRequest,
)
from ...models.update_project_machine_pool_grant_response_4xx import (
    UpdateProjectMachinePoolGrantResponse4XX,
)
from ...models.update_project_machine_pool_grant_response_5xx import (
    UpdateProjectMachinePoolGrantResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    pool_grant_id: str,
    *,
    body: UpdateProjectMachinePoolGrantRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/projects/{project_id}/machine-pool-grants/{pool_grant_id}".format(
            org_id=org_id,
            project_id=project_id,
            pool_grant_id=pool_grant_id,
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
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ProjectMachinePoolGrant.from_dict(response.json())

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
        response_4xx = UpdateProjectMachinePoolGrantResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateProjectMachinePoolGrantResponse5XX.from_dict(
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
        Error,
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
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
    pool_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMachinePoolGrantRequest,
) -> Response[
    Union[
        Error,
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
    ]
]:
    """Update project machine pool grant

     Updates the grant's overrides and limits. Omitted fields keep their current values; null clears an
    override so the grant follows the machine pool again. Overlay objects and metadata are replaced
    whole when present. Existing machines keep their configuration; the updated defaults and limits
    apply to new launches.

    Args:
        org_id (str):
        project_id (str):
        pool_grant_id (str):
        body (UpdateProjectMachinePoolGrantRequest): Update a project machine pool grant. Omitted
            fields keep their current values. Null clears an override so the grant follows the machine
            pool again. Overlay objects and metadata are replaced whole when present; send an empty
            object to clear them.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectMachinePoolGrant, UpdateProjectMachinePoolGrantResponse4XX, UpdateProjectMachinePoolGrantResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        pool_grant_id=pool_grant_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    pool_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMachinePoolGrantRequest,
) -> Optional[
    Union[
        Error,
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
    ]
]:
    """Update project machine pool grant

     Updates the grant's overrides and limits. Omitted fields keep their current values; null clears an
    override so the grant follows the machine pool again. Overlay objects and metadata are replaced
    whole when present. Existing machines keep their configuration; the updated defaults and limits
    apply to new launches.

    Args:
        org_id (str):
        project_id (str):
        pool_grant_id (str):
        body (UpdateProjectMachinePoolGrantRequest): Update a project machine pool grant. Omitted
            fields keep their current values. Null clears an override so the grant follows the machine
            pool again. Overlay objects and metadata are replaced whole when present; send an empty
            object to clear them.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectMachinePoolGrant, UpdateProjectMachinePoolGrantResponse4XX, UpdateProjectMachinePoolGrantResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        pool_grant_id=pool_grant_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    pool_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMachinePoolGrantRequest,
) -> Response[
    Union[
        Error,
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
    ]
]:
    """Update project machine pool grant

     Updates the grant's overrides and limits. Omitted fields keep their current values; null clears an
    override so the grant follows the machine pool again. Overlay objects and metadata are replaced
    whole when present. Existing machines keep their configuration; the updated defaults and limits
    apply to new launches.

    Args:
        org_id (str):
        project_id (str):
        pool_grant_id (str):
        body (UpdateProjectMachinePoolGrantRequest): Update a project machine pool grant. Omitted
            fields keep their current values. Null clears an override so the grant follows the machine
            pool again. Overlay objects and metadata are replaced whole when present; send an empty
            object to clear them.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectMachinePoolGrant, UpdateProjectMachinePoolGrantResponse4XX, UpdateProjectMachinePoolGrantResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        pool_grant_id=pool_grant_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    pool_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMachinePoolGrantRequest,
) -> Optional[
    Union[
        Error,
        ProjectMachinePoolGrant,
        UpdateProjectMachinePoolGrantResponse4XX,
        UpdateProjectMachinePoolGrantResponse5XX,
    ]
]:
    """Update project machine pool grant

     Updates the grant's overrides and limits. Omitted fields keep their current values; null clears an
    override so the grant follows the machine pool again. Overlay objects and metadata are replaced
    whole when present. Existing machines keep their configuration; the updated defaults and limits
    apply to new launches.

    Args:
        org_id (str):
        project_id (str):
        pool_grant_id (str):
        body (UpdateProjectMachinePoolGrantRequest): Update a project machine pool grant. Omitted
            fields keep their current values. Null clears an override so the grant follows the machine
            pool again. Overlay objects and metadata are replaced whole when present; send an empty
            object to clear them.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectMachinePoolGrant, UpdateProjectMachinePoolGrantResponse4XX, UpdateProjectMachinePoolGrantResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            pool_grant_id=pool_grant_id,
            client=client,
            body=body,
        )
    ).parsed
