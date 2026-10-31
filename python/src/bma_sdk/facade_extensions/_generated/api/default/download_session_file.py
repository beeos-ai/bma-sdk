from http import HTTPStatus
from io import BytesIO
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    session_id: str,
    file_id: str,
    *,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_project_id, Unset):
        headers["x-bma-project-id"] = x_bma_project_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions/{session_id}/files/{file_id}/content".format(
            session_id=session_id,
            file_id=file_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[ErrorEnvelope, File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorEnvelope, File]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, File]]:
    """Download one session file (BMA extension)

     Streams one file's bytes. `file_id` is the `id` returned by the upload
    or list operations. The response carries `Content-Type`,
    `Content-Length` and `Content-Disposition` when known, and
    `X-BMA-File-Digest` with the sha256 of the bytes. A file of another
    session, or an unknown id, is a 404 `not_found_error`.

    Args:
        session_id (str):
        file_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, File]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        file_id=file_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, File]]:
    """Download one session file (BMA extension)

     Streams one file's bytes. `file_id` is the `id` returned by the upload
    or list operations. The response carries `Content-Type`,
    `Content-Length` and `Content-Disposition` when known, and
    `X-BMA-File-Digest` with the sha256 of the bytes. A file of another
    session, or an unknown id, is a 404 `not_found_error`.

    Args:
        session_id (str):
        file_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, File]
    """

    return sync_detailed(
        session_id=session_id,
        file_id=file_id,
        client=client,
        x_bma_project_id=x_bma_project_id,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, File]]:
    """Download one session file (BMA extension)

     Streams one file's bytes. `file_id` is the `id` returned by the upload
    or list operations. The response carries `Content-Type`,
    `Content-Length` and `Content-Disposition` when known, and
    `X-BMA-File-Digest` with the sha256 of the bytes. A file of another
    session, or an unknown id, is a 404 `not_found_error`.

    Args:
        session_id (str):
        file_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, File]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        file_id=file_id,
        x_bma_project_id=x_bma_project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, File]]:
    """Download one session file (BMA extension)

     Streams one file's bytes. `file_id` is the `id` returned by the upload
    or list operations. The response carries `Content-Type`,
    `Content-Length` and `Content-Disposition` when known, and
    `X-BMA-File-Digest` with the sha256 of the bytes. A file of another
    session, or an unknown id, is a 404 `not_found_error`.

    Args:
        session_id (str):
        file_id (str):
        x_bma_project_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, File]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            file_id=file_id,
            client=client,
            x_bma_project_id=x_bma_project_id,
        )
    ).parsed
