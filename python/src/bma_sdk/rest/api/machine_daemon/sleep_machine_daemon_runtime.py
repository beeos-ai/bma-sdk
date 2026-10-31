from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daemon_runtime import DaemonRuntime
from ...models.error import Error
from ...models.sleep_machine_daemon_runtime_response_4xx import (
    SleepMachineDaemonRuntimeResponse4XX,
)
from ...models.sleep_machine_daemon_runtime_response_5xx import (
    SleepMachineDaemonRuntimeResponse5XX,
)
from ...types import Response


def _get_kwargs(
    runtime_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/daemon/runtimes/{runtime_id}/sleep".format(
            runtime_id=runtime_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    if response.status_code == 200:
        response_200 = DaemonRuntime.from_dict(response.json())

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

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = SleepMachineDaemonRuntimeResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = SleepMachineDaemonRuntimeResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Sleep machine daemon runtime

     Gracefully ends the daemon runtime and marks the machine asleep so new work queues and triggers an
    automatic wake. Rejected with 409 code pending_work when the machine has queued or live daemon work,
    and 409 code not_wake_capable when the machine has no sandbox URL.

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonRuntime, Error, SleepMachineDaemonRuntimeResponse4XX, SleepMachineDaemonRuntimeResponse5XX]]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Sleep machine daemon runtime

     Gracefully ends the daemon runtime and marks the machine asleep so new work queues and triggers an
    automatic wake. Rejected with 409 code pending_work when the machine has queued or live daemon work,
    and 409 code not_wake_capable when the machine has no sandbox URL.

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonRuntime, Error, SleepMachineDaemonRuntimeResponse4XX, SleepMachineDaemonRuntimeResponse5XX]
    """

    return sync_detailed(
        runtime_id=runtime_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Sleep machine daemon runtime

     Gracefully ends the daemon runtime and marks the machine asleep so new work queues and triggers an
    automatic wake. Rejected with 409 code pending_work when the machine has queued or live daemon work,
    and 409 code not_wake_capable when the machine has no sandbox URL.

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DaemonRuntime, Error, SleepMachineDaemonRuntimeResponse4XX, SleepMachineDaemonRuntimeResponse5XX]]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DaemonRuntime,
        Error,
        SleepMachineDaemonRuntimeResponse4XX,
        SleepMachineDaemonRuntimeResponse5XX,
    ]
]:
    """Sleep machine daemon runtime

     Gracefully ends the daemon runtime and marks the machine asleep so new work queues and triggers an
    automatic wake. Rejected with 409 code pending_work when the machine has queued or live daemon work,
    and 409 code not_wake_capable when the machine has no sandbox URL.

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DaemonRuntime, Error, SleepMachineDaemonRuntimeResponse4XX, SleepMachineDaemonRuntimeResponse5XX]
    """

    return (
        await asyncio_detailed(
            runtime_id=runtime_id,
            client=client,
        )
    ).parsed
