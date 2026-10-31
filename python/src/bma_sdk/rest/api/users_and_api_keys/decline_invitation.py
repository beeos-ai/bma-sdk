from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decline_invitation_response_4xx import DeclineInvitationResponse4XX
from ...models.decline_invitation_response_5xx import DeclineInvitationResponse5XX
from ...models.error import Error
from ...models.org_invitation import OrgInvitation
from ...types import Response


def _get_kwargs(
    invitation_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/invitations/{invitation_id}/decline".format(
            invitation_id=invitation_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    if response.status_code == 200:
        response_200 = OrgInvitation.from_dict(response.json())

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
        response_4xx = DeclineInvitationResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeclineInvitationResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    """Decline invitation

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation]]
    """

    kwargs = _get_kwargs(
        invitation_id=invitation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    """Decline invitation

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation]
    """

    return sync_detailed(
        invitation_id=invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    """Decline invitation

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation]]
    """

    kwargs = _get_kwargs(
        invitation_id=invitation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation
    ]
]:
    """Decline invitation

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeclineInvitationResponse4XX, DeclineInvitationResponse5XX, Error, OrgInvitation]
    """

    return (
        await asyncio_detailed(
            invitation_id=invitation_id,
            client=client,
        )
    ).parsed
