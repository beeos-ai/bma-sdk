from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_current_user_response_4xx import DeleteCurrentUserResponse4XX
from ...models.delete_current_user_response_5xx import DeleteCurrentUserResponse5XX
from ...models.error import Error
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/me",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
        response_4xx = DeleteCurrentUserResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteCurrentUserResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
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
) -> Response[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
]:
    """Delete the authenticated user's account

     Deletes the account, revokes all personal access tokens and browser sessions, removes all
    organization and project memberships, and releases the account's sign-in identity (emails, linked
    auth identities, and password credentials) so the same email can register a new account. Personal
    secrets and skills owned by the user are deleted with the account. Deletion is blocked while the
    user is the last owner of any organization (add another owner or delete the organization first),
    while a personal skill is referenced by an active agent's configuration, or while a personal secret
    is referenced by a model provider config, machine pool, or integration. Organization and project
    resources are unaffected, and agents, machines, and other records the user created are kept with
    their attribution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
]:
    """Delete the authenticated user's account

     Deletes the account, revokes all personal access tokens and browser sessions, removes all
    organization and project memberships, and releases the account's sign-in identity (emails, linked
    auth identities, and password credentials) so the same email can register a new account. Personal
    secrets and skills owned by the user are deleted with the account. Deletion is blocked while the
    user is the last owner of any organization (add another owner or delete the organization first),
    while a personal skill is referenced by an active agent's configuration, or while a personal secret
    is referenced by a model provider config, machine pool, or integration. Organization and project
    resources are unaffected, and agents, machines, and other records the user created are kept with
    their attribution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
]:
    """Delete the authenticated user's account

     Deletes the account, revokes all personal access tokens and browser sessions, removes all
    organization and project memberships, and releases the account's sign-in identity (emails, linked
    auth identities, and password credentials) so the same email can register a new account. Personal
    secrets and skills owned by the user are deleted with the account. Deletion is blocked while the
    user is the last owner of any organization (add another owner or delete the organization first),
    while a personal skill is referenced by an active agent's configuration, or while a personal secret
    is referenced by a model provider config, machine pool, or integration. Organization and project
    resources are unaffected, and agents, machines, and other records the user created are kept with
    their attribution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
]:
    """Delete the authenticated user's account

     Deletes the account, revokes all personal access tokens and browser sessions, removes all
    organization and project memberships, and releases the account's sign-in identity (emails, linked
    auth identities, and password credentials) so the same email can register a new account. Personal
    secrets and skills owned by the user are deleted with the account. Deletion is blocked while the
    user is the last owner of any organization (add another owner or delete the organization first),
    while a personal skill is referenced by an active agent's configuration, or while a personal secret
    is referenced by a model provider config, machine pool, or integration. Organization and project
    resources are unaffected, and agents, machines, and other records the user created are kept with
    their attribution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteCurrentUserResponse4XX, DeleteCurrentUserResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
