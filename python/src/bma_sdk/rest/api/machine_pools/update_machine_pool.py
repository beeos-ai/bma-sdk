from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.machine_pool import MachinePool
from ...models.update_machine_pool_request import UpdateMachinePoolRequest
from ...models.update_machine_pool_response_4xx import UpdateMachinePoolResponse4XX
from ...models.update_machine_pool_response_5xx import UpdateMachinePoolResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    pool_id: str,
    *,
    body: UpdateMachinePoolRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/orgs/{org_id}/machine-pools/{pool_id}".format(
            org_id=org_id,
            pool_id=pool_id,
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
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
    ]
]:
    if response.status_code == 200:
        response_200 = MachinePool.from_dict(response.json())

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
        response_4xx = UpdateMachinePoolResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateMachinePoolResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
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
    pool_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateMachinePoolRequest,
) -> Response[
    Union[
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
    ]
]:
    """Update machine pool

     Tenant-managed pools support every request field. Cluster-managed pools only allow changes to
    default CPU and memory, environment and secret environment variables, provider-supported per-machine
    CPU and memory limits, and the idle deletion policy. Other cluster-managed changes are rejected with
    409 Conflict.

    Args:
        org_id (str):
        pool_id (str):
        body (UpdateMachinePoolRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        pool_id=pool_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    pool_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateMachinePoolRequest,
) -> Optional[
    Union[
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
    ]
]:
    """Update machine pool

     Tenant-managed pools support every request field. Cluster-managed pools only allow changes to
    default CPU and memory, environment and secret environment variables, provider-supported per-machine
    CPU and memory limits, and the idle deletion policy. Other cluster-managed changes are rejected with
    409 Conflict.

    Args:
        org_id (str):
        pool_id (str):
        body (UpdateMachinePoolRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        pool_id=pool_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    pool_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateMachinePoolRequest,
) -> Response[
    Union[
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
    ]
]:
    """Update machine pool

     Tenant-managed pools support every request field. Cluster-managed pools only allow changes to
    default CPU and memory, environment and secret environment variables, provider-supported per-machine
    CPU and memory limits, and the idle deletion policy. Other cluster-managed changes are rejected with
    409 Conflict.

    Args:
        org_id (str):
        pool_id (str):
        body (UpdateMachinePoolRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        pool_id=pool_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    pool_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateMachinePoolRequest,
) -> Optional[
    Union[
        Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX
    ]
]:
    """Update machine pool

     Tenant-managed pools support every request field. Cluster-managed pools only allow changes to
    default CPU and memory, environment and secret environment variables, provider-supported per-machine
    CPU and memory limits, and the idle deletion policy. Other cluster-managed changes are rejected with
    409 Conflict.

    Args:
        org_id (str):
        pool_id (str):
        body (UpdateMachinePoolRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MachinePool, UpdateMachinePoolResponse4XX, UpdateMachinePoolResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            pool_id=pool_id,
            client=client,
            body=body,
        )
    ).parsed
