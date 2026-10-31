from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.file_list import FileList
from ...models.list_files_response_4xx import ListFilesResponse4XX
from ...models.list_files_response_5xx import ListFilesResponse5XX
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    project_id: str,
    *,
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, str] = UNSET,
    scope_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["page"] = page

    params["scope_id"] = scope_id

    json_metadata: Union[Unset, list[str]] = UNSET
    if not isinstance(metadata, Unset):
        json_metadata = metadata

    params["metadata"] = json_metadata

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/files".format(
            org_id=org_id,
            project_id=project_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
    if response.status_code == 200:
        response_200 = FileList.from_dict(response.json())

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
        response_4xx = ListFilesResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = ListFilesResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
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
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, str] = UNSET,
    scope_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
    """List files

     Lists the project's files, newest first. scope_id keeps the files scoped to one session (the files
    it produced); each metadata filter (key:value) must match a label of the file. Session instances
    created by mounting a file are never listed; read them through the session's resources.

    Args:
        org_id (str):
        project_id (str):
        limit (Union[Unset, int]):
        page (Union[Unset, str]):
        scope_id (Union[Unset, str]):
        metadata (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        limit=limit,
        page=page,
        scope_id=scope_id,
        metadata=metadata,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, str] = UNSET,
    scope_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
    """List files

     Lists the project's files, newest first. scope_id keeps the files scoped to one session (the files
    it produced); each metadata filter (key:value) must match a label of the file. Session instances
    created by mounting a file are never listed; read them through the session's resources.

    Args:
        org_id (str):
        project_id (str):
        limit (Union[Unset, int]):
        page (Union[Unset, str]):
        scope_id (Union[Unset, str]):
        metadata (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        client=client,
        limit=limit,
        page=page,
        scope_id=scope_id,
        metadata=metadata,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, str] = UNSET,
    scope_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
    """List files

     Lists the project's files, newest first. scope_id keeps the files scoped to one session (the files
    it produced); each metadata filter (key:value) must match a label of the file. Session instances
    created by mounting a file are never listed; read them through the session's resources.

    Args:
        org_id (str):
        project_id (str):
        limit (Union[Unset, int]):
        page (Union[Unset, str]):
        scope_id (Union[Unset, str]):
        metadata (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        limit=limit,
        page=page,
        scope_id=scope_id,
        metadata=metadata,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, str] = UNSET,
    scope_id: Union[Unset, str] = UNSET,
    metadata: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]]:
    """List files

     Lists the project's files, newest first. scope_id keeps the files scoped to one session (the files
    it produced); each metadata filter (key:value) must match a label of the file. Session instances
    created by mounting a file are never listed; read them through the session's resources.

    Args:
        org_id (str):
        project_id (str):
        limit (Union[Unset, int]):
        page (Union[Unset, str]):
        scope_id (Union[Unset, str]):
        metadata (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, FileList, ListFilesResponse4XX, ListFilesResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            client=client,
            limit=limit,
            page=page,
            scope_id=scope_id,
            metadata=metadata,
        )
    ).parsed
