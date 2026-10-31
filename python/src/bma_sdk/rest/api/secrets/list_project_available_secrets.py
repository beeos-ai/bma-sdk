from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_project_available_secrets_availability_source import (
    ListProjectAvailableSecretsAvailabilitySource,
)
from ...models.list_project_available_secrets_metadata import (
    ListProjectAvailableSecretsMetadata,
)
from ...models.list_project_available_secrets_owner_kind import (
    ListProjectAvailableSecretsOwnerKind,
)
from ...models.list_project_available_secrets_response_4xx import (
    ListProjectAvailableSecretsResponse4XX,
)
from ...models.list_project_available_secrets_response_5xx import (
    ListProjectAvailableSecretsResponse5XX,
)
from ...models.list_project_secret_accesses_response import (
    ListProjectSecretAccessesResponse,
)
from ...models.resource_list_sort import ResourceListSort
from ...models.secret_kind import SecretKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListProjectAvailableSecretsOwnerKind] = UNSET,
    availability_source: Union[
        Unset, ListProjectAvailableSecretsAvailabilitySource
    ] = UNSET,
    metadata: Union[Unset, "ListProjectAvailableSecretsMetadata"] = UNSET,
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

    json_availability_source: Union[Unset, str] = UNSET
    if not isinstance(availability_source, Unset):
        json_availability_source = availability_source

    params["availability_source"] = json_availability_source

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
        "url": "/orgs/{org_id}/projects/{project_id}/secrets".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
    ]
]:
    if response.status_code == 200:
        response_200 = ListProjectSecretAccessesResponse.from_dict(response.json())

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
        response_4xx = ListProjectAvailableSecretsResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListProjectAvailableSecretsResponse5XX.from_dict(response.json())

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
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
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
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListProjectAvailableSecretsOwnerKind] = UNSET,
    availability_source: Union[
        Unset, ListProjectAvailableSecretsAvailabilitySource
    ] = UNSET,
    metadata: Union[Unset, "ListProjectAvailableSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
    ]
]:
    """List secrets available to project

     Includes directly owned and granted secrets, ordered by created_at descending, then id descending.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListProjectAvailableSecretsOwnerKind]):
        availability_source (Union[Unset, ListProjectAvailableSecretsAvailabilitySource]):
        metadata (Union[Unset, ListProjectAvailableSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListProjectAvailableSecretsResponse4XX, ListProjectAvailableSecretsResponse5XX, ListProjectSecretAccessesResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        availability_source=availability_source,
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
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListProjectAvailableSecretsOwnerKind] = UNSET,
    availability_source: Union[
        Unset, ListProjectAvailableSecretsAvailabilitySource
    ] = UNSET,
    metadata: Union[Unset, "ListProjectAvailableSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
    ]
]:
    """List secrets available to project

     Includes directly owned and granted secrets, ordered by created_at descending, then id descending.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListProjectAvailableSecretsOwnerKind]):
        availability_source (Union[Unset, ListProjectAvailableSecretsAvailabilitySource]):
        metadata (Union[Unset, ListProjectAvailableSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListProjectAvailableSecretsResponse4XX, ListProjectAvailableSecretsResponse5XX, ListProjectSecretAccessesResponse]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        availability_source=availability_source,
        metadata=metadata,
        sort=sort,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListProjectAvailableSecretsOwnerKind] = UNSET,
    availability_source: Union[
        Unset, ListProjectAvailableSecretsAvailabilitySource
    ] = UNSET,
    metadata: Union[Unset, "ListProjectAvailableSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
    ]
]:
    """List secrets available to project

     Includes directly owned and granted secrets, ordered by created_at descending, then id descending.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListProjectAvailableSecretsOwnerKind]):
        availability_source (Union[Unset, ListProjectAvailableSecretsAvailabilitySource]):
        metadata (Union[Unset, ListProjectAvailableSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListProjectAvailableSecretsResponse4XX, ListProjectAvailableSecretsResponse5XX, ListProjectSecretAccessesResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        name=name,
        kind=kind,
        owner_kind=owner_kind,
        availability_source=availability_source,
        metadata=metadata,
        sort=sort,
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
    name: Union[Unset, str] = UNSET,
    kind: Union[Unset, SecretKind] = UNSET,
    owner_kind: Union[Unset, ListProjectAvailableSecretsOwnerKind] = UNSET,
    availability_source: Union[
        Unset, ListProjectAvailableSecretsAvailabilitySource
    ] = UNSET,
    metadata: Union[Unset, "ListProjectAvailableSecretsMetadata"] = UNSET,
    sort: Union[Unset, ResourceListSort] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListProjectAvailableSecretsResponse4XX,
        ListProjectAvailableSecretsResponse5XX,
        ListProjectSecretAccessesResponse,
    ]
]:
    """List secrets available to project

     Includes directly owned and granted secrets, ordered by created_at descending, then id descending.

    Args:
        org_id (str):
        project_id (str):
        name (Union[Unset, str]):
        kind (Union[Unset, SecretKind]):
        owner_kind (Union[Unset, ListProjectAvailableSecretsOwnerKind]):
        availability_source (Union[Unset, ListProjectAvailableSecretsAvailabilitySource]):
        metadata (Union[Unset, ListProjectAvailableSecretsMetadata]):
        sort (Union[Unset, ResourceListSort]): Sort order for named resources that expose created
            and modified timestamps.
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListProjectAvailableSecretsResponse4XX, ListProjectAvailableSecretsResponse5XX, ListProjectSecretAccessesResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            name=name,
            kind=kind,
            owner_kind=owner_kind,
            availability_source=availability_source,
            metadata=metadata,
            sort=sort,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
