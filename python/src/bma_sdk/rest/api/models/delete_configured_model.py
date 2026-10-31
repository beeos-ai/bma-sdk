from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_configured_model_response_4xx import (
    DeleteConfiguredModelResponse4XX,
)
from ...models.delete_configured_model_response_5xx import (
    DeleteConfiguredModelResponse5XX,
)
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/orgs/{org_id}/model-provider-configs/{model_provider_config_id}/models/{configured_model_id}".format(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            configured_model_id=configured_model_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
    ]
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
        response_4xx = DeleteConfiguredModelResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteConfiguredModelResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
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
) -> Response[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
    ]
]:
    """Delete configured model

     Deletes only the configured model. Deletion is blocked while it has active project grants. Cluster-
    managed configured models cannot be deleted through this route.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
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
) -> Optional[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
    ]
]:
    """Delete configured model

     Deletes only the configured model. Deletion is blocked while it has active project grants. Cluster-
    managed configured models cannot be deleted through this route.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error]
    """

    return sync_detailed(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
    ]
]:
    """Delete configured model

     Deletes only the configured model. Deletion is blocked while it has active project grants. Cluster-
    managed configured models cannot be deleted through this route.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        configured_model_id=configured_model_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    model_provider_config_id: str,
    configured_model_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error
    ]
]:
    """Delete configured model

     Deletes only the configured model. Deletion is blocked while it has active project grants. Cluster-
    managed configured models cannot be deleted through this route.

    Args:
        org_id (str):
        model_provider_config_id (str):
        configured_model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteConfiguredModelResponse4XX, DeleteConfiguredModelResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            configured_model_id=configured_model_id,
            client=client,
        )
    ).parsed
