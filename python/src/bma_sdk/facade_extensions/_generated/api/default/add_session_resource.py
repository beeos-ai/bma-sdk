from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.file_resource import FileResource
from ...models.file_resource_params import FileResourceParams
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    body: FileResourceParams,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_bma_project_id, Unset):
        headers["x-bma-project-id"] = x_bma_project_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sessions/{session_id}/resources".format(
            session_id=session_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[ErrorEnvelope, FileResource]:
    if response.status_code == 200:
        response_200 = FileResource.from_dict(response.json())

        return response_200

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorEnvelope, FileResource]]:
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
    body: FileResourceParams,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, FileResource]]:
    """Mount one project file into the session (BMA extension)

     Mounts an uploaded project file by reference. The Anthropic contract
    mounts files through `resources` on `POST /v1/sessions`; this extension
    mounts into an existing session. The file is read-only at `mount_path`
    (default `/mnt/session/uploads/<file_id>`), and the response `file_id`
    is the session instance created for the mount, not the project file's
    own id.

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, FileResource]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
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
    body: FileResourceParams,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, FileResource]]:
    """Mount one project file into the session (BMA extension)

     Mounts an uploaded project file by reference. The Anthropic contract
    mounts files through `resources` on `POST /v1/sessions`; this extension
    mounts into an existing session. The file is read-only at `mount_path`
    (default `/mnt/session/uploads/<file_id>`), and the response `file_id`
    is the session instance created for the mount, not the project file's
    own id.

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, FileResource]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        body=body,
        x_bma_project_id=x_bma_project_id,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: FileResourceParams,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorEnvelope, FileResource]]:
    """Mount one project file into the session (BMA extension)

     Mounts an uploaded project file by reference. The Anthropic contract
    mounts files through `resources` on `POST /v1/sessions`; this extension
    mounts into an existing session. The file is read-only at `mount_path`
    (default `/mnt/session/uploads/<file_id>`), and the response `file_id`
    is the session instance created for the mount, not the project file's
    own id.

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorEnvelope, FileResource]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
        x_bma_project_id=x_bma_project_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: FileResourceParams,
    x_bma_project_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorEnvelope, FileResource]]:
    """Mount one project file into the session (BMA extension)

     Mounts an uploaded project file by reference. The Anthropic contract
    mounts files through `resources` on `POST /v1/sessions`; this extension
    mounts into an existing session. The file is read-only at `mount_path`
    (default `/mnt/session/uploads/<file_id>`), and the response `file_id`
    is the session instance created for the mount, not the project file's
    own id.

    Args:
        session_id (str):
        x_bma_project_id (Union[Unset, str]):
        body (FileResourceParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorEnvelope, FileResource]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            body=body,
            x_bma_project_id=x_bma_project_id,
        )
    ).parsed
