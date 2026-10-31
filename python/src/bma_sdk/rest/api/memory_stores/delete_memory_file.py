from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_memory_file_response_4xx import DeleteMemoryFileResponse4XX
from ...models.delete_memory_file_response_5xx import DeleteMemoryFileResponse5XX
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    path: str,
    expected_digest: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["path"] = path

    params["expected_digest"] = expected_digest

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/orgs/{org_id}/projects/{project_id}/memory-stores/{memory_store_id}/file".format(
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
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
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
        response_4xx = DeleteMemoryFileResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = DeleteMemoryFileResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
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
    path: str,
    expected_digest: str,
) -> Response[
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
]:
    """Delete memory file

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (str):
        expected_digest (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        path=path,
        expected_digest=expected_digest,
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
    path: str,
    expected_digest: str,
) -> Optional[
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
]:
    """Delete memory file

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (str):
        expected_digest (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
    """

    return sync_detailed(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        client=client,
        path=path,
        expected_digest=expected_digest,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: str,
    expected_digest: str,
) -> Response[
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
]:
    """Delete memory file

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (str):
        expected_digest (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        project_id=project_id,
        memory_store_id=memory_store_id,
        path=path,
        expected_digest=expected_digest,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    project_id: str,
    memory_store_id: str,
    *,
    client: AuthenticatedClient,
    path: str,
    expected_digest: str,
) -> Optional[
    Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
]:
    """Delete memory file

    Args:
        org_id (str):
        project_id (str): Project ID (proj_...).
        memory_store_id (str):
        path (str):
        expected_digest (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteMemoryFileResponse4XX, DeleteMemoryFileResponse5XX, Error]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            memory_store_id=memory_store_id,
            client=client,
            path=path,
            expected_digest=expected_digest,
        )
    ).parsed
