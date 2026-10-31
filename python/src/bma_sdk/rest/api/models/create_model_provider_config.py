from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_model_provider_config_request import (
    CreateModelProviderConfigRequest,
)
from ...models.create_model_provider_config_response import (
    CreateModelProviderConfigResponse,
)
from ...models.create_model_provider_config_response_4xx import (
    CreateModelProviderConfigResponse4XX,
)
from ...models.create_model_provider_config_response_5xx import (
    CreateModelProviderConfigResponse5XX,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: CreateModelProviderConfigRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/model-provider-configs".format(
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
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
        Error,
    ]
]:
    if response.status_code == 201:
        response_201 = CreateModelProviderConfigResponse.from_dict(response.json())

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
        response_4xx = CreateModelProviderConfigResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateModelProviderConfigResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
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
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateModelProviderConfigRequest,
) -> Response[
    Union[
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
        Error,
    ]
]:
    """Create model provider config

     Create a model provider config, validate the configured credential where the provider exposes a
    validation endpoint, then probe the provider's /models endpoint. The result is returned as
    model_catalog; a failed probe does not fail creation.

    Args:
        org_id (str):
        body (CreateModelProviderConfigRequest): Connect BMA to a model API endpoint. Use a preset
            for built-in providers, or provide api_format and base_url for a custom endpoint. When
            omitted, endpoint_path and auth settings are filled from api_format.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateModelProviderConfigResponse, CreateModelProviderConfigResponse4XX, CreateModelProviderConfigResponse5XX, Error]]
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
    body: CreateModelProviderConfigRequest,
) -> Optional[
    Union[
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
        Error,
    ]
]:
    """Create model provider config

     Create a model provider config, validate the configured credential where the provider exposes a
    validation endpoint, then probe the provider's /models endpoint. The result is returned as
    model_catalog; a failed probe does not fail creation.

    Args:
        org_id (str):
        body (CreateModelProviderConfigRequest): Connect BMA to a model API endpoint. Use a preset
            for built-in providers, or provide api_format and base_url for a custom endpoint. When
            omitted, endpoint_path and auth settings are filled from api_format.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateModelProviderConfigResponse, CreateModelProviderConfigResponse4XX, CreateModelProviderConfigResponse5XX, Error]
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
    body: CreateModelProviderConfigRequest,
) -> Response[
    Union[
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
        Error,
    ]
]:
    """Create model provider config

     Create a model provider config, validate the configured credential where the provider exposes a
    validation endpoint, then probe the provider's /models endpoint. The result is returned as
    model_catalog; a failed probe does not fail creation.

    Args:
        org_id (str):
        body (CreateModelProviderConfigRequest): Connect BMA to a model API endpoint. Use a preset
            for built-in providers, or provide api_format and base_url for a custom endpoint. When
            omitted, endpoint_path and auth settings are filled from api_format.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateModelProviderConfigResponse, CreateModelProviderConfigResponse4XX, CreateModelProviderConfigResponse5XX, Error]]
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
    body: CreateModelProviderConfigRequest,
) -> Optional[
    Union[
        CreateModelProviderConfigResponse,
        CreateModelProviderConfigResponse4XX,
        CreateModelProviderConfigResponse5XX,
        Error,
    ]
]:
    """Create model provider config

     Create a model provider config, validate the configured credential where the provider exposes a
    validation endpoint, then probe the provider's /models endpoint. The result is returned as
    model_catalog; a failed probe does not fail creation.

    Args:
        org_id (str):
        body (CreateModelProviderConfigRequest): Connect BMA to a model API endpoint. Use a preset
            for built-in providers, or provide api_format and base_url for a custom endpoint. When
            omitted, endpoint_path and auth settings are filled from api_format.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateModelProviderConfigResponse, CreateModelProviderConfigResponse4XX, CreateModelProviderConfigResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
