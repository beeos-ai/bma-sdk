from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.actor_provider import ActorProvider
from ...models.error import Error
from ...models.list_actors_response import ListActorsResponse
from ...models.list_actors_response_4xx import ListActorsResponse4XX
from ...models.list_actors_response_5xx import ListActorsResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    provider: Union[Unset, ActorProvider] = UNSET,
    provider_tenant_id: Union[Unset, str] = UNSET,
    provider_user_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_provider: Union[Unset, str] = UNSET
    if not isinstance(provider, Unset):
        json_provider = provider

    params["provider"] = json_provider

    params["provider_tenant_id"] = provider_tenant_id

    params["provider_user_id"] = provider_user_id

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/actors".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
]:
    if response.status_code == 200:
        response_200 = ListActorsResponse.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListActorsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListActorsResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
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
    client: Union[AuthenticatedClient, Client],
    provider: Union[Unset, ActorProvider] = UNSET,
    provider_tenant_id: Union[Unset, str] = UNSET,
    provider_user_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
]:
    """List project actors

     Items are ordered by created_at ascending, then id ascending.

    Args:
        org_id (str):
        project_id (str):
        provider (Union[Unset, ActorProvider]): bma for BMA identities, integration for hosted
            integration senders, or external for API-managed actors.
        provider_tenant_id (Union[Unset, str]):
        provider_user_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        provider=provider,
        provider_tenant_id=provider_tenant_id,
        provider_user_id=provider_user_id,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    provider: Union[Unset, ActorProvider] = UNSET,
    provider_tenant_id: Union[Unset, str] = UNSET,
    provider_user_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
]:
    """List project actors

     Items are ordered by created_at ascending, then id ascending.

    Args:
        org_id (str):
        project_id (str):
        provider (Union[Unset, ActorProvider]): bma for BMA identities, integration for hosted
            integration senders, or external for API-managed actors.
        provider_tenant_id (Union[Unset, str]):
        provider_user_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        provider=provider,
        provider_tenant_id=provider_tenant_id,
        provider_user_id=provider_user_id,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    provider: Union[Unset, ActorProvider] = UNSET,
    provider_tenant_id: Union[Unset, str] = UNSET,
    provider_user_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
]:
    """List project actors

     Items are ordered by created_at ascending, then id ascending.

    Args:
        org_id (str):
        project_id (str):
        provider (Union[Unset, ActorProvider]): bma for BMA identities, integration for hosted
            integration senders, or external for API-managed actors.
        provider_tenant_id (Union[Unset, str]):
        provider_user_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        provider=provider,
        provider_tenant_id=provider_tenant_id,
        provider_user_id=provider_user_id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    provider: Union[Unset, ActorProvider] = UNSET,
    provider_tenant_id: Union[Unset, str] = UNSET,
    provider_user_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
]:
    """List project actors

     Items are ordered by created_at ascending, then id ascending.

    Args:
        org_id (str):
        project_id (str):
        provider (Union[Unset, ActorProvider]): bma for BMA identities, integration for hosted
            integration senders, or external for API-managed actors.
        provider_tenant_id (Union[Unset, str]):
        provider_user_id (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListActorsResponse, ListActorsResponse4XX, ListActorsResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            provider=provider,
            provider_tenant_id=provider_tenant_id,
            provider_user_id=provider_user_id,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
