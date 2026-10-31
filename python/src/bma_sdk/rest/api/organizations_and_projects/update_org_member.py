from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.organization_membership import OrganizationMembership
from ...models.update_org_member_request import UpdateOrgMemberRequest
from ...models.update_org_member_response_4xx import UpdateOrgMemberResponse4XX
from ...models.update_org_member_response_5xx import UpdateOrgMemberResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    user_id: str,
    *,
    body: UpdateOrgMemberRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/members/{user_id}".format(
            org_id=org_id,
            user_id=user_id,
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
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = OrganizationMembership.from_dict(response.json())

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
        response_4xx = UpdateOrgMemberResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateOrgMemberResponse5XX.from_dict(response.json())

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
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
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
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateOrgMemberRequest,
) -> Response[
    Union[
        Error,
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
    ]
]:
    """Update org member role

    Args:
        org_id (str):
        user_id (str):
        body (UpdateOrgMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OrganizationMembership, UpdateOrgMemberResponse4XX, UpdateOrgMemberResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateOrgMemberRequest,
) -> Optional[
    Union[
        Error,
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
    ]
]:
    """Update org member role

    Args:
        org_id (str):
        user_id (str):
        body (UpdateOrgMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OrganizationMembership, UpdateOrgMemberResponse4XX, UpdateOrgMemberResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateOrgMemberRequest,
) -> Response[
    Union[
        Error,
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
    ]
]:
    """Update org member role

    Args:
        org_id (str):
        user_id (str):
        body (UpdateOrgMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OrganizationMembership, UpdateOrgMemberResponse4XX, UpdateOrgMemberResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateOrgMemberRequest,
) -> Optional[
    Union[
        Error,
        OrganizationMembership,
        UpdateOrgMemberResponse4XX,
        UpdateOrgMemberResponse5XX,
    ]
]:
    """Update org member role

    Args:
        org_id (str):
        user_id (str):
        body (UpdateOrgMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OrganizationMembership, UpdateOrgMemberResponse4XX, UpdateOrgMemberResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
