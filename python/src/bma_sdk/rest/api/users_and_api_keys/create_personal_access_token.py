from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_personal_access_token_request import (
    CreatePersonalAccessTokenRequest,
)
from ...models.create_personal_access_token_response import (
    CreatePersonalAccessTokenResponse,
)
from ...models.create_personal_access_token_response_4xx import (
    CreatePersonalAccessTokenResponse4XX,
)
from ...models.create_personal_access_token_response_5xx import (
    CreatePersonalAccessTokenResponse5XX,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreatePersonalAccessTokenRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/personal-access-tokens",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
        Error,
    ]
]:
    if response.status_code == 201:
        response_201 = CreatePersonalAccessTokenResponse.from_dict(response.json())

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
        response_4xx = CreatePersonalAccessTokenResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreatePersonalAccessTokenResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
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
    body: CreatePersonalAccessTokenRequest,
) -> Response[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
        Error,
    ]
]:
    """Create personal access token

    Args:
        body (CreatePersonalAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreatePersonalAccessTokenResponse, CreatePersonalAccessTokenResponse4XX, CreatePersonalAccessTokenResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreatePersonalAccessTokenRequest,
) -> Optional[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
        Error,
    ]
]:
    """Create personal access token

    Args:
        body (CreatePersonalAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreatePersonalAccessTokenResponse, CreatePersonalAccessTokenResponse4XX, CreatePersonalAccessTokenResponse5XX, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreatePersonalAccessTokenRequest,
) -> Response[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
        Error,
    ]
]:
    """Create personal access token

    Args:
        body (CreatePersonalAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreatePersonalAccessTokenResponse, CreatePersonalAccessTokenResponse4XX, CreatePersonalAccessTokenResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreatePersonalAccessTokenRequest,
) -> Optional[
    Union[
        CreatePersonalAccessTokenResponse,
        CreatePersonalAccessTokenResponse4XX,
        CreatePersonalAccessTokenResponse5XX,
        Error,
    ]
]:
    """Create personal access token

    Args:
        body (CreatePersonalAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreatePersonalAccessTokenResponse, CreatePersonalAccessTokenResponse4XX, CreatePersonalAccessTokenResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
