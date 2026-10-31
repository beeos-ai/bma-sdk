from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.event_webhook import EventWebhook
from ...models.update_event_webhook_request import UpdateEventWebhookRequest
from ...models.update_event_webhook_response_4xx import UpdateEventWebhookResponse4XX
from ...models.update_event_webhook_response_5xx import UpdateEventWebhookResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    webhook_id: str,
    *,
    body: UpdateEventWebhookRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/projects/{project_id}/event-webhooks/{webhook_id}".format(
            org_id=org_id,
            project_id=project_id,
            webhook_id=webhook_id,
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
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = EventWebhook.from_dict(response.json())

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
        response_4xx = UpdateEventWebhookResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateEventWebhookResponse5XX.from_dict(response.json())

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
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
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
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateEventWebhookRequest,
) -> Response[
    Union[
        Error,
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
    ]
]:
    """Update event webhook settings

     Updates a webhook's URL, event filters, and signing settings. The scope cannot change. Omitted
    fields stay unchanged; set signing_secret_id to null to remove signing. Event filters affect newly
    queued deliveries; URL and signing changes also apply to pending attempts.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        webhook_id (str):
        body (UpdateEventWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, EventWebhook, UpdateEventWebhookResponse4XX, UpdateEventWebhookResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        webhook_id=webhook_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateEventWebhookRequest,
) -> Optional[
    Union[
        Error,
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
    ]
]:
    """Update event webhook settings

     Updates a webhook's URL, event filters, and signing settings. The scope cannot change. Omitted
    fields stay unchanged; set signing_secret_id to null to remove signing. Event filters affect newly
    queued deliveries; URL and signing changes also apply to pending attempts.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        webhook_id (str):
        body (UpdateEventWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, EventWebhook, UpdateEventWebhookResponse4XX, UpdateEventWebhookResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        webhook_id=webhook_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateEventWebhookRequest,
) -> Response[
    Union[
        Error,
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
    ]
]:
    """Update event webhook settings

     Updates a webhook's URL, event filters, and signing settings. The scope cannot change. Omitted
    fields stay unchanged; set signing_secret_id to null to remove signing. Event filters affect newly
    queued deliveries; URL and signing changes also apply to pending attempts.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        webhook_id (str):
        body (UpdateEventWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, EventWebhook, UpdateEventWebhookResponse4XX, UpdateEventWebhookResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        webhook_id=webhook_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateEventWebhookRequest,
) -> Optional[
    Union[
        Error,
        EventWebhook,
        UpdateEventWebhookResponse4XX,
        UpdateEventWebhookResponse5XX,
    ]
]:
    """Update event webhook settings

     Updates a webhook's URL, event filters, and signing settings. The scope cannot change. Omitted
    fields stay unchanged; set signing_secret_id to null to remove signing. Event filters affect newly
    queued deliveries; URL and signing changes also apply to pending attempts.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        webhook_id (str):
        body (UpdateEventWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, EventWebhook, UpdateEventWebhookResponse4XX, UpdateEventWebhookResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            webhook_id=webhook_id,
            client=client,
            body=body,
        )
    ).parsed
