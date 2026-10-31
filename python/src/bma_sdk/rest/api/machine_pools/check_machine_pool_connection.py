from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_machine_pool_connection_request import (
    CheckMachinePoolConnectionRequest,
)
from ...models.check_machine_pool_connection_response_4xx import (
    CheckMachinePoolConnectionResponse4XX,
)
from ...models.check_machine_pool_connection_response_5xx import (
    CheckMachinePoolConnectionResponse5XX,
)
from ...models.error import Error
from ...models.machine_pool_connection_check_error import (
    MachinePoolConnectionCheckError,
)
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: CheckMachinePoolConnectionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/machine-pools/check-connection".format(
            org_id=org_id,
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
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
    ]
]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 422:
        response_422 = MachinePoolConnectionCheckError.from_dict(response.json())

        return response_422

    if response.status_code == 424:
        response_424 = MachinePoolConnectionCheckError.from_dict(response.json())

        return response_424

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = CheckMachinePoolConnectionResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = CheckMachinePoolConnectionResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
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
    *,
    client: AuthenticatedClient,
    body: CheckMachinePoolConnectionRequest,
) -> Response[
    Union[
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
    ]
]:
    """Check machine pool connection

     Checks a tenant-managed pool's provider credential and provider config by making read-only requests
    to the provider.

    Args:
        org_id (str):
        body (CheckMachinePoolConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CheckMachinePoolConnectionResponse4XX, CheckMachinePoolConnectionResponse5XX, Error, MachinePoolConnectionCheckError]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CheckMachinePoolConnectionRequest,
) -> Optional[
    Union[
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
    ]
]:
    """Check machine pool connection

     Checks a tenant-managed pool's provider credential and provider config by making read-only requests
    to the provider.

    Args:
        org_id (str):
        body (CheckMachinePoolConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CheckMachinePoolConnectionResponse4XX, CheckMachinePoolConnectionResponse5XX, Error, MachinePoolConnectionCheckError]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CheckMachinePoolConnectionRequest,
) -> Response[
    Union[
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
    ]
]:
    """Check machine pool connection

     Checks a tenant-managed pool's provider credential and provider config by making read-only requests
    to the provider.

    Args:
        org_id (str):
        body (CheckMachinePoolConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CheckMachinePoolConnectionResponse4XX, CheckMachinePoolConnectionResponse5XX, Error, MachinePoolConnectionCheckError]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: CheckMachinePoolConnectionRequest,
) -> Optional[
    Union[
        Any,
        CheckMachinePoolConnectionResponse4XX,
        CheckMachinePoolConnectionResponse5XX,
        Error,
        MachinePoolConnectionCheckError,
    ]
]:
    """Check machine pool connection

     Checks a tenant-managed pool's provider credential and provider config by making read-only requests
    to the provider.

    Args:
        org_id (str):
        body (CheckMachinePoolConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CheckMachinePoolConnectionResponse4XX, CheckMachinePoolConnectionResponse5XX, Error, MachinePoolConnectionCheckError]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
