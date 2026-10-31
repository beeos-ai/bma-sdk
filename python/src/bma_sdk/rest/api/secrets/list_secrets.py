from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_secrets_metadata import ListSecretsMetadata
from ...models.list_secrets_owner_kind import (
    ListSecretsOwnerKind,
)
from ...models.list_secrets_response import ListSecretsResponse
from ...models.list_secrets_response_4xx import ListSecretsResponse4XX
from ...models.list_secrets_response_5xx import ListSecretsResponse5XX
from ...models.resource_list_sort import ResourceListSort
from ...models.secret_kind import SecretKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListSecretsOwnerKind] = UNSET,
    owner_project_id: Union[Unset, str] = UNSET,
    mcp_oauth_flow_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, "ListSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["name"] = name

    json_kind: Union[Unset, str] = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind

    params["kind"] = json_kind

    json_owner_kind: Union[Unset, str] = UNSET
    if not isinstance(owner_kind, Unset):
        json_owner_kind = owner_kind

    params["owner_kind"] = json_owner_kind

    params["owner_project_id"] = owner_project_id

    params["mcp_oauth_flow_id"] = mcp_oauth_flow_id

    json_metadata: Union[Unset, dict[str, Any]] = UNSET
    if not isinstance(metadata, Unset):
        json_metadata = metadata.to_dict()
    if not isinstance(json_metadata, Unset):
        params.update(json_metadata)

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/secrets".format(
            org_id=org_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
]:
    if response.status_code == 200:
        response_200 = ListSecretsResponse.from_dict(response.json())

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
        response_4xx = ListSecretsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListSecretsResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
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
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListSecretsOwnerKind] = UNSET,
    owner_project_id: Union[Unset, str] = UNSET,
    mcp_oauth_flow_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, "ListSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
]:
    """List secrets visible through ownership authority

     Items are ordered by created_at descending, then id descending. Without an owner filter, returns the
    deduplicated union of organization secrets the caller may list, project secrets the caller may list,
    and the caller's own user secrets.

    Args:
        org_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListSecretsOwnerKind]):
        owner_project_id (Union[Unset, str]): Project ID (proj_...).
        mcp_oauth_flow_id (Union[Unset, str]):
        metadata (Union[Unset, ListSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        owner_project_id=owner_project_id,
        mcp_oauth_flow_id=mcp_oauth_flow_id,
        metadata=metadata,
        sort=sort,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListSecretsOwnerKind] = UNSET,
    owner_project_id: Union[Unset, str] = UNSET,
    mcp_oauth_flow_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, "ListSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
]:
    """List secrets visible through ownership authority

     Items are ordered by created_at descending, then id descending. Without an owner filter, returns the
    deduplicated union of organization secrets the caller may list, project secrets the caller may list,
    and the caller's own user secrets.

    Args:
        org_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListSecretsOwnerKind]):
        owner_project_id (Union[Unset, str]): Project ID (proj_...).
        mcp_oauth_flow_id (Union[Unset, str]):
        metadata (Union[Unset, ListSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        owner_project_id=owner_project_id,
        mcp_oauth_flow_id=mcp_oauth_flow_id,
        metadata=metadata,
        sort=sort,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListSecretsOwnerKind] = UNSET,
    owner_project_id: Union[Unset, str] = UNSET,
    mcp_oauth_flow_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, "ListSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
]:
    """List secrets visible through ownership authority

     Items are ordered by created_at descending, then id descending. Without an owner filter, returns the
    deduplicated union of organization secrets the caller may list, project secrets the caller may list,
    and the caller's own user secrets.

    Args:
        org_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListSecretsOwnerKind]):
        owner_project_id (Union[Unset, str]): Project ID (proj_...).
        mcp_oauth_flow_id (Union[Unset, str]):
        metadata (Union[Unset, ListSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        owner_project_id=owner_project_id,
        mcp_oauth_flow_id=mcp_oauth_flow_id,
        metadata=metadata,
        sort=sort,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListSecretsOwnerKind] = UNSET,
    owner_project_id: Union[Unset, str] = UNSET,
    mcp_oauth_flow_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, "ListSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
]:
    """List secrets visible through ownership authority

     Items are ordered by created_at descending, then id descending. Without an owner filter, returns the
    deduplicated union of organization secrets the caller may list, project secrets the caller may list,
    and the caller's own user secrets.

    Args:
        org_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListSecretsOwnerKind]):
        owner_project_id (Union[Unset, str]): Project ID (proj_...).
        mcp_oauth_flow_id (Union[Unset, str]):
        metadata (Union[Unset, ListSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListSecretsResponse, ListSecretsResponse4XX, ListSecretsResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            name=name,
            kind=kind,
            owner_kind=owner_kind,
            owner_project_id=owner_project_id,
            mcp_oauth_flow_id=mcp_oauth_flow_id,
            metadata=metadata,
            sort=sort,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
