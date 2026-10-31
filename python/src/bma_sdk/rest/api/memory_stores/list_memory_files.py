from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_memory_files_response_4xx import ListMemoryFilesResponse4XX
from ...models.list_memory_files_response_5xx import ListMemoryFilesResponse5XX
from ...models.memory_file_list import MemoryFileList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    path: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["path"] = path

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/memory-stores/{memory_store_id}/files".format(
            org_id=org_id,
            project_id=project_id,
            memory_store_id=memory_store_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
]:
    if response.status_code == 200:
        response_200 = MemoryFileList.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = ListMemoryFilesResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListMemoryFilesResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
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
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
]:
    """List memory files

     List a directory's immediate children in name order. Omit path to list the store root.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        path=path,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
]:
    """List memory files

     List a directory's immediate children in name order. Omit path to list the store root.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        client=client,
        path=path,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Response[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
]:
    """List memory files

     List a directory's immediate children in name order. Omit path to list the store root.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        path=path,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[
    Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
]:
    """List memory files

     List a directory's immediate children in name order. Omit path to list the store root.

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListMemoryFilesResponse4XX, ListMemoryFilesResponse5XX, MemoryFileList]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            memory_store_id=memory_store_id,
            client=client,
            path=path,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
