from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_agent_request_type_0 import CreateAgentRequestType0
from ...models.create_agent_request_type_1 import CreateAgentRequestType1
from ...models.create_agent_request_type_2 import CreateAgentRequestType2
from ...models.create_agent_response_4xx import CreateAgentResponse4XX
from ...models.create_agent_response_5xx import CreateAgentResponse5XX
from ...models.current_agent_response import CurrentAgentResponse
from ...models.error import Error
from ...models.launch_agent_response import LaunchAgentResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: Union[
        "CreateAgentRequestType0", "CreateAgentRequestType1", "CreateAgentRequestType2"
    ],
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/agents".format(
            org_id=org_id,
            project_id=project_id,
        ),
    }

    _kwargs["json"]: dict[str, Any]
    if isinstance(body, CreateAgentRequestType0):
        _kwargs["json"] = body.to_dict()
    elif isinstance(body, CreateAgentRequestType1):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
    ]
]:
    if response.status_code == 200:
        response_200 = CurrentAgentResponse.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = LaunchAgentResponse.from_dict(response.json())

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
        response_4xx = CreateAgentResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CreateAgentResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
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
    client: AuthenticatedClient,
    body: Union[
        "CreateAgentRequestType0", "CreateAgentRequestType1", "CreateAgentRequestType2"
    ],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
    ]
]:
    """Create agent

     Launch from a pinned config, optionally adding agent-local integration tools, subscriptions and
    interaction handlers and admitting an attributed initial text input in the same transaction. Adding
    integration capabilities requires project management permission; launching an existing config
    requires agent operate permission. Reusing an idempotency key returns the current agent even if the
    retry body differs. The retry body is not applied and integration references are not resolved again.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (Union['CreateAgentRequestType0', 'CreateAgentRequestType1',
            'CreateAgentRequestType2']): Send at least one of profile, config, or config_source, and
            not both config and config_source. With only profile, the agent runs the profile's current
            config. With profile and config or config_source, the agent is attributed to the profile
            but runs the given config, which need not be one of the profile's versions. config_source
            is compiled and saved as a new config during the launch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateAgentResponse4XX, CreateAgentResponse5XX, CurrentAgentResponse, Error, LaunchAgentResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        "CreateAgentRequestType0", "CreateAgentRequestType1", "CreateAgentRequestType2"
    ],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
    ]
]:
    """Create agent

     Launch from a pinned config, optionally adding agent-local integration tools, subscriptions and
    interaction handlers and admitting an attributed initial text input in the same transaction. Adding
    integration capabilities requires project management permission; launching an existing config
    requires agent operate permission. Reusing an idempotency key returns the current agent even if the
    retry body differs. The retry body is not applied and integration references are not resolved again.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (Union['CreateAgentRequestType0', 'CreateAgentRequestType1',
            'CreateAgentRequestType2']): Send at least one of profile, config, or config_source, and
            not both config and config_source. With only profile, the agent runs the profile's current
            config. With profile and config or config_source, the agent is attributed to the profile
            but runs the given config, which need not be one of the profile's versions. config_source
            is compiled and saved as a new config during the launch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateAgentResponse4XX, CreateAgentResponse5XX, CurrentAgentResponse, Error, LaunchAgentResponse]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        "CreateAgentRequestType0", "CreateAgentRequestType1", "CreateAgentRequestType2"
    ],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
    ]
]:
    """Create agent

     Launch from a pinned config, optionally adding agent-local integration tools, subscriptions and
    interaction handlers and admitting an attributed initial text input in the same transaction. Adding
    integration capabilities requires project management permission; launching an existing config
    requires agent operate permission. Reusing an idempotency key returns the current agent even if the
    retry body differs. The retry body is not applied and integration references are not resolved again.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (Union['CreateAgentRequestType0', 'CreateAgentRequestType1',
            'CreateAgentRequestType2']): Send at least one of profile, config, or config_source, and
            not both config and config_source. With only profile, the agent runs the profile's current
            config. With profile and config or config_source, the agent is attributed to the profile
            but runs the given config, which need not be one of the profile's versions. config_source
            is compiled and saved as a new config during the launch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateAgentResponse4XX, CreateAgentResponse5XX, CurrentAgentResponse, Error, LaunchAgentResponse]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        "CreateAgentRequestType0", "CreateAgentRequestType1", "CreateAgentRequestType2"
    ],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateAgentResponse4XX,
        CreateAgentResponse5XX,
        CurrentAgentResponse,
        Error,
        LaunchAgentResponse,
    ]
]:
    """Create agent

     Launch from a pinned config, optionally adding agent-local integration tools, subscriptions and
    interaction handlers and admitting an attributed initial text input in the same transaction. Adding
    integration capabilities requires project management permission; launching an existing config
    requires agent operate permission. Reusing an idempotency key returns the current agent even if the
    retry body differs. The retry body is not applied and integration references are not resolved again.

    Args:
        org_id (str):
        project_id (str):
        idempotency_key (Union[Unset, str]):
        body (Union['CreateAgentRequestType0', 'CreateAgentRequestType1',
            'CreateAgentRequestType2']): Send at least one of profile, config, or config_source, and
            not both config and config_source. With only profile, the agent runs the profile's current
            config. With profile and config or config_source, the agent is attributed to the profile
            but runs the given config, which need not be one of the profile's versions. config_source
            is compiled and saved as a new config during the launch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateAgentResponse4XX, CreateAgentResponse5XX, CurrentAgentResponse, Error, LaunchAgentResponse]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
