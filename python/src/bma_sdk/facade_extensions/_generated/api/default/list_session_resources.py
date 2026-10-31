from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.file_resource_page import FileResourcePage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_project_id, Unset):
        headers["x-bma-project-id"] = x_bma_project_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions/{session_id}/resources".format(
            session_id=session_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[ErrorEnvelope, FileResourcePage]:
    if response.status_code == 200:
        response_200 = FileResourcePage.from_dict(response.json())

        return response_200

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorEnvelope, FileResourcePage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, FileResourcePage]]:
    """List the session's mounted file resources (BMA extension)

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, FileResourcePage]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, FileResourcePage]]:
    """List the session's mounted file resources (BMA extension)

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, FileResourcePage]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        x_bma_project_id=x_bma_project_id,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, FileResourcePage]]:
    """List the session's mounted file resources (BMA extension)

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, FileResourcePage]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, FileResourcePage]]:
    """List the session's mounted file resources (BMA extension)

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, FileResourcePage]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            x_bma_project_id=x_bma_project_id,
        )
    ).parsed
