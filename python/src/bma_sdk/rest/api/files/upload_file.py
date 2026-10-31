from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project_file import ProjectFile
from ...models.upload_file_response_4xx import UploadFileResponse4XX
from ...models.upload_file_response_5xx import UploadFileResponse5XX
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    body: File,
    filename: str,
    idempotency_key: Union[Unset, str] = UNSET,
    x_bma_file_metadata: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_bma_file_metadata, Unset):
        headers["X-BMA-File-Metadata"] = x_bma_file_metadata

    params: dict[str, Any] = {}

    params["filename"] = filename

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orgs/{org_id}/projects/{project_id}/files".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload

    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
    if response.status_code == 200:
        response_200 = ProjectFile.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = ProjectFile.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = UploadFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UploadFileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
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
    body: File,
    filename: str,
    idempotency_key: Union[Unset, str] = UNSET,
    x_bma_file_metadata: Union[Unset, str] = UNSET,
) -> Response[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
    """Upload a file

     Streams the request body (1 byte to 1 GiB) into object storage as a project file. A replay with the
    same Idempotency-Key, filename, content and labels returns the original file with 200; a different
    request under the key is 409. The project's files may not exceed its storage limit (409).

    Args:
        org_id (str):
        project_id (str):
        filename (str):
        idempotency_key (Union[Unset, str]):
        x_bma_file_metadata (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
        filename=filename,
        idempotency_key=idempotency_key,
        x_bma_file_metadata=x_bma_file_metadata,
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
    body: File,
    filename: str,
    idempotency_key: Union[Unset, str] = UNSET,
    x_bma_file_metadata: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
    """Upload a file

     Streams the request body (1 byte to 1 GiB) into object storage as a project file. A replay with the
    same Idempotency-Key, filename, content and labels returns the original file with 200; a different
    request under the key is 409. The project's files may not exceed its storage limit (409).

    Args:
        org_id (str):
        project_id (str):
        filename (str):
        idempotency_key (Union[Unset, str]):
        x_bma_file_metadata (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        body=body,
        filename=filename,
        idempotency_key=idempotency_key,
        x_bma_file_metadata=x_bma_file_metadata,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    filename: str,
    idempotency_key: Union[Unset, str] = UNSET,
    x_bma_file_metadata: Union[Unset, str] = UNSET,
) -> Response[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
    """Upload a file

     Streams the request body (1 byte to 1 GiB) into object storage as a project file. A replay with the
    same Idempotency-Key, filename, content and labels returns the original file with 200; a different
    request under the key is 409. The project's files may not exceed its storage limit (409).

    Args:
        org_id (str):
        project_id (str):
        filename (str):
        idempotency_key (Union[Unset, str]):
        x_bma_file_metadata (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        body=body,
        filename=filename,
        idempotency_key=idempotency_key,
        x_bma_file_metadata=x_bma_file_metadata,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    filename: str,
    idempotency_key: Union[Unset, str] = UNSET,
    x_bma_file_metadata: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]]:
    """Upload a file

     Streams the request body (1 byte to 1 GiB) into object storage as a project file. A replay with the
    same Idempotency-Key, filename, content and labels returns the original file with 200; a different
    request under the key is 409. The project's files may not exceed its storage limit (409).

    Args:
        org_id (str):
        project_id (str):
        filename (str):
        idempotency_key (Union[Unset, str]):
        x_bma_file_metadata (Union[Unset, str]):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ProjectFile, UploadFileResponse4XX, UploadFileResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            body=body,
            filename=filename,
            idempotency_key=idempotency_key,
            x_bma_file_metadata=x_bma_file_metadata,
        )
    ).parsed
