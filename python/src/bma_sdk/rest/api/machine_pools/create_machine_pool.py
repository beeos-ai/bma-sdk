from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_machine_pool_request import CreateMachinePoolRequest
from ...models.create_machine_pool_response_4xx import CreateMachinePoolResponse4XX
from ...models.create_machine_pool_response_5xx import CreateMachinePoolResponse5XX
from ...models.error import Error
from ...models.machine_pool import MachinePool
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: CreateMachinePoolRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/machine-pools".format(
            org_id=org_id,
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
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
    ]
]:
    if response.status_code == 200:
        response_200 = MachinePool.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = MachinePool.from_dict(response.json())

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
        response_4xx = CreateMachinePoolResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateMachinePoolResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
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
    *,
    client: AuthenticatedClient,
    body: CreateMachinePoolRequest,
) -> Response[
    Union[
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
    ]
]:
    """Create machine pool

    Args:
        org_id (str):
        body (CreateMachinePoolRequest): Pool definition. name, provider, provider_auth_secret_id,
            default_machine_provider_options, and max_total_machines are always required; which
            default machine size and CPU and memory limits are required depends on the provider;
            Blaxel pools reject CPU fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateMachinePoolRequest,
) -> Optional[
    Union[
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
    ]
]:
    """Create machine pool

    Args:
        org_id (str):
        body (CreateMachinePoolRequest): Pool definition. name, provider, provider_auth_secret_id,
            default_machine_provider_options, and max_total_machines are always required; which
            default machine size and CPU and memory limits are required depends on the provider;
            Blaxel pools reject CPU fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateMachinePoolRequest,
) -> Response[
    Union[
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
    ]
]:
    """Create machine pool

    Args:
        org_id (str):
        body (CreateMachinePoolRequest): Pool definition. name, provider, provider_auth_secret_id,
            default_machine_provider_options, and max_total_machines are always required; which
            default machine size and CPU and memory limits are required depends on the provider;
            Blaxel pools reject CPU fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateMachinePoolRequest,
) -> Optional[
    Union[
        CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool
    ]
]:
    """Create machine pool

    Args:
        org_id (str):
        body (CreateMachinePoolRequest): Pool definition. name, provider, provider_auth_secret_id,
            default_machine_provider_options, and max_total_machines are always required; which
            default machine size and CPU and memory limits are required depends on the provider;
            Blaxel pools reject CPU fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateMachinePoolResponse4XX, CreateMachinePoolResponse5XX, Error, MachinePool]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
