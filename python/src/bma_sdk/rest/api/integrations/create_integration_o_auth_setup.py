from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_integration_o_auth_setup_request import (
    CreateIntegrationOAuthSetupRequest,
)
from ...models.create_integration_o_auth_setup_response_4xx import (
    CreateIntegrationOAuthSetupResponse4XX,
)
from ...models.create_integration_o_auth_setup_response_5xx import (
    CreateIntegrationOAuthSetupResponse5XX,
)
from ...models.error import Error
from ...models.integration_o_auth_setup import IntegrationOAuthSetup
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    integration_id: str,
    *,
    body: CreateIntegrationOAuthSetupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/integrations/{integration_id}/oauth/setup".format(
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
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
    ]
]:
    if response.status_code == 201:
        response_201 = IntegrationOAuthSetup.from_dict(response.json())

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
        response_4xx = CreateIntegrationOAuthSetupResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateIntegrationOAuthSetupResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
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
    body: CreateIntegrationOAuthSetupRequest,
) -> Response[
    Union[
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
    ]
]:
    """Connect an integration through OAuth

     Starts OAuth for this integration (currently Slack). The callback pins the integration and setup
    revision, records verified credentials, and returns integration_oauth=success and integration_id to
    the supplied local return_to route. It requires a browser session for the initiating user and
    current project management access. Replayed, stale, or deleted-integration callbacks are rejected.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateIntegrationOAuthSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateIntegrationOAuthSetupResponse4XX, CreateIntegrationOAuthSetupResponse5XX, Error, IntegrationOAuthSetup]]
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
    body: CreateIntegrationOAuthSetupRequest,
) -> Optional[
    Union[
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
    ]
]:
    """Connect an integration through OAuth

     Starts OAuth for this integration (currently Slack). The callback pins the integration and setup
    revision, records verified credentials, and returns integration_oauth=success and integration_id to
    the supplied local return_to route. It requires a browser session for the initiating user and
    current project management access. Replayed, stale, or deleted-integration callbacks are rejected.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateIntegrationOAuthSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateIntegrationOAuthSetupResponse4XX, CreateIntegrationOAuthSetupResponse5XX, Error, IntegrationOAuthSetup]
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
    body: CreateIntegrationOAuthSetupRequest,
) -> Response[
    Union[
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
    ]
]:
    """Connect an integration through OAuth

     Starts OAuth for this integration (currently Slack). The callback pins the integration and setup
    revision, records verified credentials, and returns integration_oauth=success and integration_id to
    the supplied local return_to route. It requires a browser session for the initiating user and
    current project management access. Replayed, stale, or deleted-integration callbacks are rejected.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateIntegrationOAuthSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateIntegrationOAuthSetupResponse4XX, CreateIntegrationOAuthSetupResponse5XX, Error, IntegrationOAuthSetup]]
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
    body: CreateIntegrationOAuthSetupRequest,
) -> Optional[
    Union[
        CreateIntegrationOAuthSetupResponse4XX,
        CreateIntegrationOAuthSetupResponse5XX,
        Error,
        IntegrationOAuthSetup,
    ]
]:
    """Connect an integration through OAuth

     Starts OAuth for this integration (currently Slack). The callback pins the integration and setup
    revision, records verified credentials, and returns integration_oauth=success and integration_id to
    the supplied local return_to route. It requires a browser session for the initiating user and
    current project management access. Replayed, stale, or deleted-integration callbacks are rejected.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        body (CreateIntegrationOAuthSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateIntegrationOAuthSetupResponse4XX, CreateIntegrationOAuthSetupResponse5XX, Error, IntegrationOAuthSetup]
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
