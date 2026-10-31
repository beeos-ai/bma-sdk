from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_organization_request import CreateOrganizationRequest
from ...models.create_organization_response import CreateOrganizationResponse
from ...models.create_organization_response_4xx import CreateOrganizationResponse4XX
from ...models.create_organization_response_5xx import CreateOrganizationResponse5XX
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreateOrganizationRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
        Error,
    ]
]:
    if response.status_code == 200:
        response_200 = CreateOrganizationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = CreateOrganizationResponse.from_dict(response.json())

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
        response_4xx = CreateOrganizationResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateOrganizationResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
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
    *,
    client: AuthenticatedClient,
    body: CreateOrganizationRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
        Error,
    ]
]:
    """Create organization

     Creates the organization and its local default resources atomically.
    An idempotency key determines the proposed organization ID; replaying it
    returns the existing organization. Without a key, each request is a fresh
    attempt. Optional default-provider provisioning begins after commit and
    retries asynchronously without failing organization creation.

    Args:
        idempotency_key (Union[Unset, str]):
        body (CreateOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationResponse, CreateOrganizationResponse4XX, CreateOrganizationResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateOrganizationRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
        Error,
    ]
]:
    """Create organization

     Creates the organization and its local default resources atomically.
    An idempotency key determines the proposed organization ID; replaying it
    returns the existing organization. Without a key, each request is a fresh
    attempt. Optional default-provider provisioning begins after commit and
    retries asynchronously without failing organization creation.

    Args:
        idempotency_key (Union[Unset, str]):
        body (CreateOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationResponse, CreateOrganizationResponse4XX, CreateOrganizationResponse5XX, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateOrganizationRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
        Error,
    ]
]:
    """Create organization

     Creates the organization and its local default resources atomically.
    An idempotency key determines the proposed organization ID; replaying it
    returns the existing organization. Without a key, each request is a fresh
    attempt. Optional default-provider provisioning begins after commit and
    retries asynchronously without failing organization creation.

    Args:
        idempotency_key (Union[Unset, str]):
        body (CreateOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationResponse, CreateOrganizationResponse4XX, CreateOrganizationResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateOrganizationRequest,
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateOrganizationResponse,
        CreateOrganizationResponse4XX,
        CreateOrganizationResponse5XX,
        Error,
    ]
]:
    """Create organization

     Creates the organization and its local default resources atomically.
    An idempotency key determines the proposed organization ID; replaying it
    returns the existing organization. Without a key, each request is a fresh
    attempt. Optional default-provider provisioning begins after commit and
    retries asynchronously without failing organization creation.

    Args:
        idempotency_key (Union[Unset, str]):
        body (CreateOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationResponse, CreateOrganizationResponse4XX, CreateOrganizationResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
