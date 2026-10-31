from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.event_webhook_scope_type import (
    EventWebhookScopeType,
)
from ...models.list_event_webhooks_response import ListEventWebhooksResponse
from ...models.list_event_webhooks_response_4xx import ListEventWebhooksResponse4XX
from ...models.list_event_webhooks_response_5xx import ListEventWebhooksResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    scope_type: EventWebhookScopeType,
    agent_profile_id: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_scope_type: str = scope_type
    params["scope_type"] = json_scope_type

    params["agent_profile_id"] = agent_profile_id

    params["agent_id"] = agent_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/event-webhooks".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error,
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = ListEventWebhooksResponse.from_dict(response.json())

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
        response_4xx = ListEventWebhooksResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListEventWebhooksResponse5XX.from_dict(response.json())

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
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
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
    *,
    client: Union[AuthenticatedClient, Client],
    scope_type: EventWebhookScopeType,
    agent_profile_id: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
    ]
]:
    """List event webhooks for one scope

     Returns the webhooks directly attached to the requested scope, not inherited matches.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        scope_type (EventWebhookScopeType):
        agent_profile_id (Union[Unset, str]):
        agent_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListEventWebhooksResponse, ListEventWebhooksResponse4XX, ListEventWebhooksResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        scope_type=scope_type,
        agent_profile_id=agent_profile_id,
        agent_id=agent_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    scope_type: EventWebhookScopeType,
    agent_profile_id: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
    ]
]:
    """List event webhooks for one scope

     Returns the webhooks directly attached to the requested scope, not inherited matches.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        scope_type (EventWebhookScopeType):
        agent_profile_id (Union[Unset, str]):
        agent_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListEventWebhooksResponse, ListEventWebhooksResponse4XX, ListEventWebhooksResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        scope_type=scope_type,
        agent_profile_id=agent_profile_id,
        agent_id=agent_id,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    scope_type: EventWebhookScopeType,
    agent_profile_id: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Error,
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
    ]
]:
    """List event webhooks for one scope

     Returns the webhooks directly attached to the requested scope, not inherited matches.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        scope_type (EventWebhookScopeType):
        agent_profile_id (Union[Unset, str]):
        agent_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListEventWebhooksResponse, ListEventWebhooksResponse4XX, ListEventWebhooksResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        scope_type=scope_type,
        agent_profile_id=agent_profile_id,
        agent_id=agent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    scope_type: EventWebhookScopeType,
    agent_profile_id: Union[Unset, str] = UNSET,
    agent_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Error,
        ListEventWebhooksResponse,
        ListEventWebhooksResponse4XX,
        ListEventWebhooksResponse5XX,
    ]
]:
    """List event webhooks for one scope

     Returns the webhooks directly attached to the requested scope, not inherited matches.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        scope_type (EventWebhookScopeType):
        agent_profile_id (Union[Unset, str]):
        agent_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListEventWebhooksResponse, ListEventWebhooksResponse4XX, ListEventWebhooksResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            scope_type=scope_type,
            agent_profile_id=agent_profile_id,
            agent_id=agent_id,
        )
    ).parsed
