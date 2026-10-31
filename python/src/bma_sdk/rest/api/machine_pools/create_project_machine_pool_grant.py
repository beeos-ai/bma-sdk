from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_project_machine_pool_grant_request import (
    CreateProjectMachinePoolGrantRequest,
)
from ...models.create_project_machine_pool_grant_response_4xx import (
    CreateProjectMachinePoolGrantResponse4XX,
)
from ...models.create_project_machine_pool_grant_response_5xx import (
    CreateProjectMachinePoolGrantResponse5XX,
)
from ...models.error import Error
from ...models.project_machine_pool_grant import ProjectMachinePoolGrant
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: CreateProjectMachinePoolGrantRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/machine-pool-grants".format(
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
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
    ]
]:
    if response.status_code == 200:
        response_200 = ProjectMachinePoolGrant.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = ProjectMachinePoolGrant.from_dict(response.json())

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
        response_4xx = CreateProjectMachinePoolGrantResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateProjectMachinePoolGrantResponse5XX.from_dict(
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
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
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
    body: CreateProjectMachinePoolGrantRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
    ]
]:
    """Create project machine pool grant

     Lets a project create machines from a machine pool, optionally with its own defaults and usage caps
    within the pool's limits, and returns the grant. No machines are created by this call.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (CreateProjectMachinePoolGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateProjectMachinePoolGrantResponse4XX, CreateProjectMachinePoolGrantResponse5XX, Error, ProjectMachinePoolGrant]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
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
    *,
    client: AuthenticatedClient,
    body: CreateProjectMachinePoolGrantRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
    ]
]:
    """Create project machine pool grant

     Lets a project create machines from a machine pool, optionally with its own defaults and usage caps
    within the pool's limits, and returns the grant. No machines are created by this call.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (CreateProjectMachinePoolGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateProjectMachinePoolGrantResponse4XX, CreateProjectMachinePoolGrantResponse5XX, Error, ProjectMachinePoolGrant]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectMachinePoolGrantRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
    ]
]:
    """Create project machine pool grant

     Lets a project create machines from a machine pool, optionally with its own defaults and usage caps
    within the pool's limits, and returns the grant. No machines are created by this call.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (CreateProjectMachinePoolGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateProjectMachinePoolGrantResponse4XX, CreateProjectMachinePoolGrantResponse5XX, Error, ProjectMachinePoolGrant]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectMachinePoolGrantRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateProjectMachinePoolGrantResponse4XX,
        CreateProjectMachinePoolGrantResponse5XX,
        Error,
        ProjectMachinePoolGrant,
    ]
]:
    """Create project machine pool grant

     Lets a project create machines from a machine pool, optionally with its own defaults and usage caps
    within the pool's limits, and returns the grant. No machines are created by this call.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (CreateProjectMachinePoolGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateProjectMachinePoolGrantResponse4XX, CreateProjectMachinePoolGrantResponse5XX, Error, ProjectMachinePoolGrant]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
