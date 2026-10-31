from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.model_provider_config import ModelProviderConfig
from ...models.update_model_provider_config_request import (
    UpdateModelProviderConfigRequest,
)
from ...models.update_model_provider_config_response_4xx import (
    UpdateModelProviderConfigResponse4XX,
)
from ...models.update_model_provider_config_response_5xx import (
    UpdateModelProviderConfigResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    model_provider_config_id: str,
    *,
    body: UpdateModelProviderConfigRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/orgs/{org_id}/model-provider-configs/{model_provider_config_id}".format(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
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
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ModelProviderConfig.from_dict(response.json())

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
        response_4xx = UpdateModelProviderConfigResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateModelProviderConfigResponse5XX.from_dict(response.json())

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
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
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
    model_provider_config_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateModelProviderConfigRequest,
) -> Response[
    Union[
        Error,
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
    ]
]:
    """Update model provider config

     Updates a model provider config's connection settings, such as its credential and headers, and
    returns the updated config; omitted fields keep their values. The credential secret is checked to
    exist and match auth_kind, but the provider isn't contacted, so a credential the provider rejects
    isn't caught here.

    Args:
        org_id (str):
        model_provider_config_id (str):
        body (UpdateModelProviderConfigRequest): Update a provider config. Omitted fields keep
            their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ModelProviderConfig, UpdateModelProviderConfigResponse4XX, UpdateModelProviderConfigResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateModelProviderConfigRequest,
) -> Optional[
    Union[
        Error,
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
    ]
]:
    """Update model provider config

     Updates a model provider config's connection settings, such as its credential and headers, and
    returns the updated config; omitted fields keep their values. The credential secret is checked to
    exist and match auth_kind, but the provider isn't contacted, so a credential the provider rejects
    isn't caught here.

    Args:
        org_id (str):
        model_provider_config_id (str):
        body (UpdateModelProviderConfigRequest): Update a provider config. Omitted fields keep
            their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ModelProviderConfig, UpdateModelProviderConfigResponse4XX, UpdateModelProviderConfigResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateModelProviderConfigRequest,
) -> Response[
    Union[
        Error,
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
    ]
]:
    """Update model provider config

     Updates a model provider config's connection settings, such as its credential and headers, and
    returns the updated config; omitted fields keep their values. The credential secret is checked to
    exist and match auth_kind, but the provider isn't contacted, so a credential the provider rejects
    isn't caught here.

    Args:
        org_id (str):
        model_provider_config_id (str):
        body (UpdateModelProviderConfigRequest): Update a provider config. Omitted fields keep
            their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ModelProviderConfig, UpdateModelProviderConfigResponse4XX, UpdateModelProviderConfigResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateModelProviderConfigRequest,
) -> Optional[
    Union[
        Error,
        ModelProviderConfig,
        UpdateModelProviderConfigResponse4XX,
        UpdateModelProviderConfigResponse5XX,
    ]
]:
    """Update model provider config

     Updates a model provider config's connection settings, such as its credential and headers, and
    returns the updated config; omitted fields keep their values. The credential secret is checked to
    exist and match auth_kind, but the provider isn't contacted, so a credential the provider rejects
    isn't caught here.

    Args:
        org_id (str):
        model_provider_config_id (str):
        body (UpdateModelProviderConfigRequest): Update a provider config. Omitted fields keep
            their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ModelProviderConfig, UpdateModelProviderConfigResponse4XX, UpdateModelProviderConfigResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            client=client,
            body=body,
        )
    ).parsed
