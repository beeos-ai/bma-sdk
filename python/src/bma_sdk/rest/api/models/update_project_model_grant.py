from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project_model_grant_envelope import ProjectModelGrantEnvelope
from ...models.update_project_model_grant_request import UpdateProjectModelGrantRequest
from ...models.update_project_model_grant_response_4xx import (
    UpdateProjectModelGrantResponse4XX,
)
from ...models.update_project_model_grant_response_5xx import (
    UpdateProjectModelGrantResponse5XX,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    model_grant_id: str,
    *,
    body: UpdateProjectModelGrantRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/projects/{project_id}/model-grants/{model_grant_id}".format(
            org_id=org_id,
            project_id=project_id,
            model_grant_id=model_grant_id,
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
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ProjectModelGrantEnvelope.from_dict(response.json())

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
        response_4xx = UpdateProjectModelGrantResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateProjectModelGrantResponse5XX.from_dict(response.json())

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
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
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
    model_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectModelGrantRequest,
) -> Response[
    Union[
        Error,
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
    ]
]:
    """Update project model grant

     Updates the project's overrides for the configured model. Omitted fields keep their current values;
    null, or [] for supported_reasoning_efforts, input_modalities, and output_modalities, clears an
    override so the project inherits from the configured model. Agents already using the model apply the
    updated overrides on their next model call. Updates are validated against the configured model's
    current revision but not against agent configs, so narrowing below a config's model settings, such
    as its context_window_tokens or reasoning effort, makes that agent's next model call fail.

    Args:
        org_id (str):
        project_id (str):
        model_grant_id (str):
        body (UpdateProjectModelGrantRequest): Update a project model grant's overrides. Omitted
            fields keep their current values. Null clears an override so the project inherits from the
            configured model; for arrays, an empty array clears the override.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectModelGrantEnvelope, UpdateProjectModelGrantResponse4XX, UpdateProjectModelGrantResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        model_grant_id=model_grant_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    model_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectModelGrantRequest,
) -> Optional[
    Union[
        Error,
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
    ]
]:
    """Update project model grant

     Updates the project's overrides for the configured model. Omitted fields keep their current values;
    null, or [] for supported_reasoning_efforts, input_modalities, and output_modalities, clears an
    override so the project inherits from the configured model. Agents already using the model apply the
    updated overrides on their next model call. Updates are validated against the configured model's
    current revision but not against agent configs, so narrowing below a config's model settings, such
    as its context_window_tokens or reasoning effort, makes that agent's next model call fail.

    Args:
        org_id (str):
        project_id (str):
        model_grant_id (str):
        body (UpdateProjectModelGrantRequest): Update a project model grant's overrides. Omitted
            fields keep their current values. Null clears an override so the project inherits from the
            configured model; for arrays, an empty array clears the override.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectModelGrantEnvelope, UpdateProjectModelGrantResponse4XX, UpdateProjectModelGrantResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        model_grant_id=model_grant_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    model_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectModelGrantRequest,
) -> Response[
    Union[
        Error,
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
    ]
]:
    """Update project model grant

     Updates the project's overrides for the configured model. Omitted fields keep their current values;
    null, or [] for supported_reasoning_efforts, input_modalities, and output_modalities, clears an
    override so the project inherits from the configured model. Agents already using the model apply the
    updated overrides on their next model call. Updates are validated against the configured model's
    current revision but not against agent configs, so narrowing below a config's model settings, such
    as its context_window_tokens or reasoning effort, makes that agent's next model call fail.

    Args:
        org_id (str):
        project_id (str):
        model_grant_id (str):
        body (UpdateProjectModelGrantRequest): Update a project model grant's overrides. Omitted
            fields keep their current values. Null clears an override so the project inherits from the
            configured model; for arrays, an empty array clears the override.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectModelGrantEnvelope, UpdateProjectModelGrantResponse4XX, UpdateProjectModelGrantResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        model_grant_id=model_grant_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    model_grant_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectModelGrantRequest,
) -> Optional[
    Union[
        Error,
        ProjectModelGrantEnvelope,
        UpdateProjectModelGrantResponse4XX,
        UpdateProjectModelGrantResponse5XX,
    ]
]:
    """Update project model grant

     Updates the project's overrides for the configured model. Omitted fields keep their current values;
    null, or [] for supported_reasoning_efforts, input_modalities, and output_modalities, clears an
    override so the project inherits from the configured model. Agents already using the model apply the
    updated overrides on their next model call. Updates are validated against the configured model's
    current revision but not against agent configs, so narrowing below a config's model settings, such
    as its context_window_tokens or reasoning effort, makes that agent's next model call fail.

    Args:
        org_id (str):
        project_id (str):
        model_grant_id (str):
        body (UpdateProjectModelGrantRequest): Update a project model grant's overrides. Omitted
            fields keep their current values. Null clears an override so the project inherits from the
            configured model; for arrays, an empty array clears the override.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectModelGrantEnvelope, UpdateProjectModelGrantResponse4XX, UpdateProjectModelGrantResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            model_grant_id=model_grant_id,
            client=client,
            body=body,
        )
    ).parsed
