from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configured_model import ConfiguredModel
from ...models.error import Error
from ...models.update_configured_model_request import UpdateConfiguredModelRequest
from ...models.update_configured_model_response_4xx import (
    UpdateConfiguredModelResponse4XX,
)
from ...models.update_configured_model_response_5xx import (
    UpdateConfiguredModelResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    body: UpdateConfiguredModelRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/orgs/{org_id}/model-provider-configs/{model_provider_config_id}/models/{configured_model_id}".format(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            configured_model_id=configured_model_id,
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
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ConfiguredModel.from_dict(response.json())

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
        response_4xx = UpdateConfiguredModelResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateConfiguredModelResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
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
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConfiguredModelRequest,
) -> Response[
    Union[
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
    ]
]:
    """Update configured model

     Updates a configured model's settings and returns the updated model; omitted fields keep their
    values. Agents already using the model pick up the change on their next model call. The update isn't
    checked against project grants or agent configs, so lowering a limit below their overrides or
    turning off tools or reasoning they rely on makes those agents' next model call fail.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):
        body (UpdateConfiguredModelRequest): Update a configured model. Omitted fields keep their
            current values. Runtime changes create a new immutable model revision; changing only name
            just renames the model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfiguredModel, Error, UpdateConfiguredModelResponse4XX, UpdateConfiguredModelResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConfiguredModelRequest,
) -> Optional[
    Union[
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
    ]
]:
    """Update configured model

     Updates a configured model's settings and returns the updated model; omitted fields keep their
    values. Agents already using the model pick up the change on their next model call. The update isn't
    checked against project grants or agent configs, so lowering a limit below their overrides or
    turning off tools or reasoning they rely on makes those agents' next model call fail.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):
        body (UpdateConfiguredModelRequest): Update a configured model. Omitted fields keep their
            current values. Runtime changes create a new immutable model revision; changing only name
            just renames the model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConfiguredModel, Error, UpdateConfiguredModelResponse4XX, UpdateConfiguredModelResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConfiguredModelRequest,
) -> Response[
    Union[
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
    ]
]:
    """Update configured model

     Updates a configured model's settings and returns the updated model; omitted fields keep their
    values. Agents already using the model pick up the change on their next model call. The update isn't
    checked against project grants or agent configs, so lowering a limit below their overrides or
    turning off tools or reasoning they rely on makes those agents' next model call fail.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):
        body (UpdateConfiguredModelRequest): Update a configured model. Omitted fields keep their
            current values. Runtime changes create a new immutable model revision; changing only name
            just renames the model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfiguredModel, Error, UpdateConfiguredModelResponse4XX, UpdateConfiguredModelResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateConfiguredModelRequest,
) -> Optional[
    Union[
        ConfiguredModel,
        Error,
        UpdateConfiguredModelResponse4XX,
        UpdateConfiguredModelResponse5XX,
    ]
]:
    """Update configured model

     Updates a configured model's settings and returns the updated model; omitted fields keep their
    values. Agents already using the model pick up the change on their next model call. The update isn't
    checked against project grants or agent configs, so lowering a limit below their overrides or
    turning off tools or reasoning they rely on makes those agents' next model call fail.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):
        body (UpdateConfiguredModelRequest): Update a configured model. Omitted fields keep their
            current values. Runtime changes create a new immutable model revision; changing only name
            just renames the model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConfiguredModel, Error, UpdateConfiguredModelResponse4XX, UpdateConfiguredModelResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            configured_model_id=configured_model_id,
            client=client,
            body=body,
        )
    ).parsed
