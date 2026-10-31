from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_file_content_response_4xx import GetFileContentResponse4XX
from ...models.get_file_content_response_5xx import GetFileContentResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    project_id: str,
    file_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orgs/{org_id}/projects/{project_id}/files/{file_id}/content".format(
            org_id=org_id,
            project_id=project_id,
            file_id=file_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
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
        response_4xx = GetFileContentResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetFileContentResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
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
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
    """Download a file

     Streams the file content with its length and SHA-256 digest.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
    """Download a file

     Streams the file content with its length and SHA-256 digest.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]
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
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
    """Download a file

     Streams the file content with its length and SHA-256 digest.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]]:
    """Download a file

     Streams the file content with its length and SHA-256 digest.

    Args:
        org_id (str):
        project_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetFileContentResponse4XX, GetFileContentResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            project_id=project_id,
            file_id=file_id,
            client=client,
        )
    ).parsed
