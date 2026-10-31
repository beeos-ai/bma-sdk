from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.deleted_session_resource import DeletedSessionResource
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    resource_id: str,
    *,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_project_id, Unset):
        headers["x-bma-project-id"] = x_bma_project_id

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/sessions/{session_id}/resources/{resource_id}".format(
            session_id=session_id,
            resource_id=resource_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DeletedSessionResource, ErrorEnvelope]:
    if response.status_code == 200:
        response_200 = DeletedSessionResource.from_dict(response.json())

        return response_200

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeletedSessionResource, ErrorEnvelope]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    resource_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[DeletedSessionResource, ErrorEnvelope]]:
    """Unmount one file resource from the session (BMA extension)

     Removes the mount and releases the session instance. The project file
    itself is kept; other sessions that mounted it keep their instances.

    Args:
        session_id (str):
        resource_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeletedSessionResource, ErrorEnvelope]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        resource_id=resource_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    resource_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DeletedSessionResource, ErrorEnvelope]]:
    """Unmount one file resource from the session (BMA extension)

     Removes the mount and releases the session instance. The project file
    itself is kept; other sessions that mounted it keep their instances.

    Args:
        session_id (str):
        resource_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeletedSessionResource, ErrorEnvelope]
    """

    return sync_detailed(
        session_id=session_id,
        resource_id=resource_id,
        client=client,
        x_bma_project_id=x_bma_project_id,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    resource_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[DeletedSessionResource, ErrorEnvelope]]:
    """Unmount one file resource from the session (BMA extension)

     Removes the mount and releases the session instance. The project file
    itself is kept; other sessions that mounted it keep their instances.

    Args:
        session_id (str):
        resource_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeletedSessionResource, ErrorEnvelope]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        resource_id=resource_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    resource_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DeletedSessionResource, ErrorEnvelope]]:
    """Unmount one file resource from the session (BMA extension)

     Removes the mount and releases the session instance. The project file
    itself is kept; other sessions that mounted it keep their instances.

    Args:
        session_id (str):
        resource_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeletedSessionResource, ErrorEnvelope]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            resource_id=resource_id,
            client=client,
            x_bma_project_id=x_bma_project_id,
        )
    ).parsed
