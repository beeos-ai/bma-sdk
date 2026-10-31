from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_model_catalog_response_4xx import GetModelCatalogResponse4XX
from ...models.get_model_catalog_response_5xx import GetModelCatalogResponse5XX
from ...models.model_catalog import ModelCatalog
from ...types import Response


def _get_kwargs(
    org_id: str,
    model_provider_config_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/model-provider-configs/{model_provider_config_id}/model-catalog".format(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
]:
    if response.status_code == 200:
        response_200 = ModelCatalog.from_dict(response.json())

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
        response_4xx = GetModelCatalogResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetModelCatalogResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
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
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
]:
    """Get model catalog

     Fetches the provider's live model catalog by validating the configured credential and probing the
    provider's /models endpoint. The call waits on the upstream provider, so it is slower than the other
    model provider config routes and can report failure as data.

    Args:
        org_id (str):
        model_provider_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
]:
    """Get model catalog

     Fetches the provider's live model catalog by validating the configured credential and probing the
    provider's /models endpoint. The call waits on the upstream provider, so it is slower than the other
    model provider config routes and can report failure as data.

    Args:
        org_id (str):
        model_provider_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
    """

    return sync_detailed(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
]:
    """Get model catalog

     Fetches the provider's live model catalog by validating the configured credential and probing the
    provider's /models endpoint. The call waits on the upstream provider, so it is slower than the other
    model provider config routes and can report failure as data.

    Args:
        org_id (str):
        model_provider_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        model_provider_config_id=model_provider_config_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    model_provider_config_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
]:
    """Get model catalog

     Fetches the provider's live model catalog by validating the configured credential and probing the
    provider's /models endpoint. The call waits on the upstream provider, so it is slower than the other
    model provider config routes and can report failure as data.

    Args:
        org_id (str):
        model_provider_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetModelCatalogResponse4XX, GetModelCatalogResponse5XX, ModelCatalog]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            client=client,
        )
    ).parsed
