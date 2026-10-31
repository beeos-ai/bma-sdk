from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_git_hub_setup_request import CreateGitHubSetupRequest
from ...models.create_integration_git_hub_setup_response_4xx import (
    CreateIntegrationGitHubSetupResponse4XX,
)
from ...models.create_integration_git_hub_setup_response_5xx import (
    CreateIntegrationGitHubSetupResponse5XX,
)
from ...models.error import Error
from ...models.git_hub_setup import GitHubSetup
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    body: CreateGitHubSetupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/integrations/{integration_id}/github-setup".format(
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
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
    ]
]:
    if response.status_code == 201:
        response_201 = GitHubSetup.from_dict(response.json())

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
        response_4xx = CreateIntegrationGitHubSetupResponse4XX.from_dict(
            response.json()
        )

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateIntegrationGitHubSetupResponse5XX.from_dict(
            response.json()
        )

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
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
    body: CreateGitHubSetupRequest,
) -> Response[
    Union[
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
    ]
]:
    """Start registration of a customer-owned GitHub App

     Starts guided registration on github.com for a never-connected GitHub integration. Requires a
    browser session and project management access. Submit manifest as a JSON-encoded form field to
    registration_url. The callback saves a project credential secret and redirects to the canonical
    integration page with github_setup=credentials_saved and credential_secret_id (a public secret ID).
    It does not connect an installation or change launcher settings.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateGitHubSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateIntegrationGitHubSetupResponse4XX, CreateIntegrationGitHubSetupResponse5XX, Error, GitHubSetup]]
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
    body: CreateGitHubSetupRequest,
) -> Optional[
    Union[
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
    ]
]:
    """Start registration of a customer-owned GitHub App

     Starts guided registration on github.com for a never-connected GitHub integration. Requires a
    browser session and project management access. Submit manifest as a JSON-encoded form field to
    registration_url. The callback saves a project credential secret and redirects to the canonical
    integration page with github_setup=credentials_saved and credential_secret_id (a public secret ID).
    It does not connect an installation or change launcher settings.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateGitHubSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateIntegrationGitHubSetupResponse4XX, CreateIntegrationGitHubSetupResponse5XX, Error, GitHubSetup]
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
    body: CreateGitHubSetupRequest,
) -> Response[
    Union[
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
    ]
]:
    """Start registration of a customer-owned GitHub App

     Starts guided registration on github.com for a never-connected GitHub integration. Requires a
    browser session and project management access. Submit manifest as a JSON-encoded form field to
    registration_url. The callback saves a project credential secret and redirects to the canonical
    integration page with github_setup=credentials_saved and credential_secret_id (a public secret ID).
    It does not connect an installation or change launcher settings.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateGitHubSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateIntegrationGitHubSetupResponse4XX, CreateIntegrationGitHubSetupResponse5XX, Error, GitHubSetup]]
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
    body: CreateGitHubSetupRequest,
) -> Optional[
    Union[
        CreateIntegrationGitHubSetupResponse4XX,
        CreateIntegrationGitHubSetupResponse5XX,
        Error,
        GitHubSetup,
    ]
]:
    """Start registration of a customer-owned GitHub App

     Starts guided registration on github.com for a never-connected GitHub integration. Requires a
    browser session and project management access. Submit manifest as a JSON-encoded form field to
    registration_url. The callback saves a project credential secret and redirects to the canonical
    integration page with github_setup=credentials_saved and credential_secret_id (a public secret ID).
    It does not connect an installation or change launcher settings.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateGitHubSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateIntegrationGitHubSetupResponse4XX, CreateIntegrationGitHubSetupResponse5XX, Error, GitHubSetup]
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
