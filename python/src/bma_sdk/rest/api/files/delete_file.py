from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_file_response_4xx import DeleteFileResponse4XX
from ...models.delete_file_response_5xx import DeleteFileResponse5XX
from ...models.deleted_file import DeletedFile
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    file_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/orgs/{org_id}/projects/{project_id}/files/{file_id}".format(
            org_id=org_id,
            project_id=project_id,
            file_id=file_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    if response.status_code == 200:
        response_200 = DeletedFile.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = DeleteFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteFileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    project_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    """Delete a file

     Deletes the file: it is no longer readable, listable or mountable. Sessions that mounted it keep
    reading their own session instance until the resource is removed or the session is archived; the
    stored content is reclaimed after the last of them. Deleting a session instance removes its session
    resource. Artifacts the file was promoted from are kept.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    """Delete a file

     Deletes the file: it is no longer readable, listable or mountable. Sessions that mounted it keep
    reading their own session instance until the resource is removed or the session is archived; the
    stored content is reclaimed after the last of them. Deleting a session instance removes its session
    resource. Artifacts the file was promoted from are kept.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    """Delete a file

     Deletes the file: it is no longer readable, listable or mountable. Sessions that mounted it keep
    reading their own session instance until the resource is removed or the session is archived; the
    stored content is reclaimed after the last of them. Deleting a session instance removes its session
    resource. Artifacts the file was promoted from are kept.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    file_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]]:
    """Delete a file

     Deletes the file: it is no longer readable, listable or mountable. Sessions that mounted it keep
    reading their own session instance until the resource is removed or the session is archived; the
    stored content is reclaimed after the last of them. Deleting a session instance removes its session
    resource. Artifacts the file was promoted from are kept.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteFileResponse4XX, DeleteFileResponse5XX, DeletedFile, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            file_id=file_id,
            client=client,
        )
    ).parsed
