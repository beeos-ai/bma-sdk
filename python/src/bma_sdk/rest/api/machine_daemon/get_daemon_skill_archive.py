from http import HTTPStatus
from io import BytesIO
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_daemon_skill_archive_response_4xx import (
    GetDaemonSkillArchiveResponse4XX,
)
from ...models.get_daemon_skill_archive_response_5xx import (
    GetDaemonSkillArchiveResponse5XX,
)
from ...types import UNSET, File, Response


def _get_kwargs(
    skill_id: str,
    *,
    revision_id: str,
    expires_at: int,
    download_token: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["revision_id"] = revision_id

    params["expires_at"] = expires_at

    params["download_token"] = download_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/daemon/skills/{skill_id}/archive".format(
            skill_id=skill_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if 400 <= response.status_code <= 499:
        response_4xx = GetDaemonSkillArchiveResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = GetDaemonSkillArchiveResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_id: str,
    *,
    client: AuthenticatedClient,
    revision_id: str,
    expires_at: int,
    download_token: str,
) -> Response[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    """Get daemon skill archive

     Requires daemon authentication plus a short-lived capability bound to the authenticated machine,
    skill, and revision.

    Args:
        skill_id (str):
        revision_id (str):
        expires_at (int):
        download_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX]]
    """

    kwargs = _get_kwargs(
        skill_id=skill_id,
        revision_id=revision_id,
        expires_at=expires_at,
        download_token=download_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    skill_id: str,
    *,
    client: AuthenticatedClient,
    revision_id: str,
    expires_at: int,
    download_token: str,
) -> Optional[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    """Get daemon skill archive

     Requires daemon authentication plus a short-lived capability bound to the authenticated machine,
    skill, and revision.

    Args:
        skill_id (str):
        revision_id (str):
        expires_at (int):
        download_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX]
    """

    return sync_detailed(
        skill_id=skill_id,
        client=client,
        revision_id=revision_id,
        expires_at=expires_at,
        download_token=download_token,
    ).parsed


async def asyncio_detailed(
    skill_id: str,
    *,
    client: AuthenticatedClient,
    revision_id: str,
    expires_at: int,
    download_token: str,
) -> Response[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    """Get daemon skill archive

     Requires daemon authentication plus a short-lived capability bound to the authenticated machine,
    skill, and revision.

    Args:
        skill_id (str):
        revision_id (str):
        expires_at (int):
        download_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX]]
    """

    kwargs = _get_kwargs(
        skill_id=skill_id,
        revision_id=revision_id,
        expires_at=expires_at,
        download_token=download_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    skill_id: str,
    *,
    client: AuthenticatedClient,
    revision_id: str,
    expires_at: int,
    download_token: str,
) -> Optional[
    Union[
        Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX
    ]
]:
    """Get daemon skill archive

     Requires daemon authentication plus a short-lived capability bound to the authenticated machine,
    skill, and revision.

    Args:
        skill_id (str):
        revision_id (str):
        expires_at (int):
        download_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, File, GetDaemonSkillArchiveResponse4XX, GetDaemonSkillArchiveResponse5XX]
    """

    return (
        await asyncio_detailed(
            skill_id=skill_id,
            client=client,
            revision_id=revision_id,
            expires_at=expires_at,
            download_token=download_token,
        )
    ).parsed
