from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configure_integration_request import ConfigureIntegrationRequest
from ...models.configure_integration_response_4xx import ConfigureIntegrationResponse4XX
from ...models.configure_integration_response_5xx import ConfigureIntegrationResponse5XX
from ...models.error import Error
from ...models.integration import Integration
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    body: ConfigureIntegrationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/integrations/{integration_id}/setup".format(
            org_id=org_id,
            project_id=project_id,
            integration_id=integration_id,
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
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
    ]
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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ConfigureIntegrationResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ConfigureIntegrationResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
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
    project_id: str,
    integration_id: str,
    *,
    client: AuthenticatedClient,
    body: ConfigureIntegrationRequest,
) -> Response[
    Union[
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
    ]
]:
    """Verify and configure integration credentials

     Requires a user principal with project management permission. Slack credentials are configured
    through OAuth. A stale expected_setup_revision or a credential changed during verification returns
    409; reload the integration and retry setup. Setup preserves integration settings; verified provider
    identity scopes incoming events.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (ConfigureIntegrationRequest): Verifies credentials for this saved integration.
            GitHub tenant/account are the numeric App ID and Installation ID; the secret is
            github_app_credentials. Discord tenant is the Application ID; its generic secret contains
            the bot token, from which the bot User ID is discovered automatically. Reconnect preserves
            the original verified provider identity. A concurrent setup change rejects this request.
            Credential payloads are never returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfigureIntegrationResponse4XX, ConfigureIntegrationResponse5XX, Error, Integration]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
        body=body,
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
    client: AuthenticatedClient,
    body: ConfigureIntegrationRequest,
) -> Optional[
    Union[
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
    ]
]:
    """Verify and configure integration credentials

     Requires a user principal with project management permission. Slack credentials are configured
    through OAuth. A stale expected_setup_revision or a credential changed during verification returns
    409; reload the integration and retry setup. Setup preserves integration settings; verified provider
    identity scopes incoming events.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (ConfigureIntegrationRequest): Verifies credentials for this saved integration.
            GitHub tenant/account are the numeric App ID and Installation ID; the secret is
            github_app_credentials. Discord tenant is the Application ID; its generic secret contains
            the bot token, from which the bot User ID is discovered automatically. Reconnect preserves
            the original verified provider identity. A concurrent setup change rejects this request.
            Credential payloads are never returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConfigureIntegrationResponse4XX, ConfigureIntegrationResponse5XX, Error, Integration]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: AuthenticatedClient,
    body: ConfigureIntegrationRequest,
) -> Response[
    Union[
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
    ]
]:
    """Verify and configure integration credentials

     Requires a user principal with project management permission. Slack credentials are configured
    through OAuth. A stale expected_setup_revision or a credential changed during verification returns
    409; reload the integration and retry setup. Setup preserves integration settings; verified provider
    identity scopes incoming events.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (ConfigureIntegrationRequest): Verifies credentials for this saved integration.
            GitHub tenant/account are the numeric App ID and Installation ID; the secret is
            github_app_credentials. Discord tenant is the Application ID; its generic secret contains
            the bot token, from which the bot User ID is discovered automatically. Reconnect preserves
            the original verified provider identity. A concurrent setup change rejects this request.
            Credential payloads are never returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfigureIntegrationResponse4XX, ConfigureIntegrationResponse5XX, Error, Integration]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        integration_id=integration_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    client: AuthenticatedClient,
    body: ConfigureIntegrationRequest,
) -> Optional[
    Union[
        ConfigureIntegrationResponse4XX,
        ConfigureIntegrationResponse5XX,
        Error,
        Integration,
    ]
]:
    """Verify and configure integration credentials

     Requires a user principal with project management permission. Slack credentials are configured
    through OAuth. A stale expected_setup_revision or a credential changed during verification returns
    409; reload the integration and retry setup. Setup preserves integration settings; verified provider
    identity scopes incoming events.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (ConfigureIntegrationRequest): Verifies credentials for this saved integration.
            GitHub tenant/account are the numeric App ID and Installation ID; the secret is
            github_app_credentials. Discord tenant is the Application ID; its generic secret contains
            the bot token, from which the bot User ID is discovered automatically. Reconnect preserves
            the original verified provider identity. A concurrent setup change rejects this request.
            Credential payloads are never returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ConfigureIntegrationResponse4XX, ConfigureIntegrationResponse5XX, Error, Integration]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            integration_id=integration_id,
            client=client,
            body=body,
        )
    ).parsed
