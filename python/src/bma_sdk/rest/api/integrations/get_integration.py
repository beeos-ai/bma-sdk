from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_integration_response_4xx import GetIntegrationResponse4XX
from ...models.get_integration_response_5xx import GetIntegrationResponse5XX
from ...models.integration import Integration
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    integration_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/integrations/{integration_id}".format(
            org_id=org_id,
            project_id=project_id,
            integration_id=integration_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    if response.status_code == 200:
        response_200 = Integration.from_dict(response.json())

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

    if 400 <= response.status_code <= 499:
        response_4xx = GetIntegrationResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetIntegrationResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    """Get project integration

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    """Get project integration

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    """Get project integration

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
]:
    """Get project integration

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetIntegrationResponse4XX, GetIntegrationResponse5XX, Integration]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            integration_id=integration_id,
            client=client,
        )
    ).parsed
