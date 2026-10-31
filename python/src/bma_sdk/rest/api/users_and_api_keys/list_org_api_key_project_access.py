from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_org_api_key_project_access_response_4xx import (
    ListOrgAPIKeyProjectAccessResponse4XX,
)
from ...models.list_org_api_key_project_access_response_5xx import (
    ListOrgAPIKeyProjectAccessResponse5XX,
)
from ...models.list_project_membership_grants_response import (
    ListProjectMembershipGrantsResponse,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    key_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/api-keys/{key_id}/projects".format(
            org_id=org_id,
            key_id=key_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
    ]
]:
    if response.status_code == 200:
        response_200 = ListProjectMembershipGrantsResponse.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListOrgAPIKeyProjectAccessResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListOrgAPIKeyProjectAccessResponse5XX.from_dict(response.json())

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
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
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
    key_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        Error,
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
    ]
]:
    """List an org API key's explicit project role grants

     Lists the key's explicit per-project role grants. Keys with the admin org role implicitly have admin
    access to every project and will not appear here for those projects.

    Args:
        org_id (str):
        key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListOrgAPIKeyProjectAccessResponse4XX, ListOrgAPIKeyProjectAccessResponse5XX, ListProjectMembershipGrantsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        key_id=key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    key_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        Error,
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
    ]
]:
    """List an org API key's explicit project role grants

     Lists the key's explicit per-project role grants. Keys with the admin org role implicitly have admin
    access to every project and will not appear here for those projects.

    Args:
        org_id (str):
        key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListOrgAPIKeyProjectAccessResponse4XX, ListOrgAPIKeyProjectAccessResponse5XX, ListProjectMembershipGrantsResponse]
    """

    return sync_detailed(
        org_id=org_id,
        key_id=key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    key_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        Error,
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
    ]
]:
    """List an org API key's explicit project role grants

     Lists the key's explicit per-project role grants. Keys with the admin org role implicitly have admin
    access to every project and will not appear here for those projects.

    Args:
        org_id (str):
        key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListOrgAPIKeyProjectAccessResponse4XX, ListOrgAPIKeyProjectAccessResponse5XX, ListProjectMembershipGrantsResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        key_id=key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    key_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        Error,
        ListOrgAPIKeyProjectAccessResponse4XX,
        ListOrgAPIKeyProjectAccessResponse5XX,
        ListProjectMembershipGrantsResponse,
    ]
]:
    """List an org API key's explicit project role grants

     Lists the key's explicit per-project role grants. Keys with the admin org role implicitly have admin
    access to every project and will not appear here for those projects.

    Args:
        org_id (str):
        key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListOrgAPIKeyProjectAccessResponse4XX, ListOrgAPIKeyProjectAccessResponse5XX, ListProjectMembershipGrantsResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            key_id=key_id,
            client=client,
        )
    ).parsed
