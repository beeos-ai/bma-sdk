from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.secret import Secret
from ...models.update_secret_request import UpdateSecretRequest
from ...models.update_secret_response_4xx import UpdateSecretResponse4XX
from ...models.update_secret_response_5xx import UpdateSecretResponse5XX
from ...types import Response


def _get_kwargs(
    org_id: str,
    secret_id: str,
    *,
    body: UpdateSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/orgs/{org_id}/secrets/{secret_id}".format(
            org_id=org_id,
            secret_id=secret_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    if response.status_code == 200:
        response_200 = Secret.from_dict(response.json())

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
        response_4xx = UpdateSecretResponse4XX.from_dict(response.json())

        return response_4xx

    if 500 <= response.status_code <= 599:
        response_5xx = UpdateSecretResponse5XX.from_dict(response.json())

        return response_5xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Response[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    """Update secret metadata

     Renames a secret or replaces its metadata, and returns the updated secret without its value. The
    value, kind, and owner can't be changed here. References use the secret ID, so renaming doesn't
    break them.

    Args:
        org_id (str):
        secret_id (str):
        body (UpdateSecretRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        secret_id=secret_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Optional[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    """Update secret metadata

     Renames a secret or replaces its metadata, and returns the updated secret without its value. The
    value, kind, and owner can't be changed here. References use the secret ID, so renaming doesn't
    break them.

    Args:
        org_id (str):
        secret_id (str):
        body (UpdateSecretRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]
    """

    return sync_detailed(
        org_id=org_id,
        secret_id=secret_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Response[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    """Update secret metadata

     Renames a secret or replaces its metadata, and returns the updated secret without its value. The
    value, kind, and owner can't be changed here. References use the secret ID, so renaming doesn't
    break them.

    Args:
        org_id (str):
        secret_id (str):
        body (UpdateSecretRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        secret_id=secret_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateSecretRequest,
) -> Optional[Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]]:
    """Update secret metadata

     Renames a secret or replaces its metadata, and returns the updated secret without its value. The
    value, kind, and owner can't be changed here. References use the secret ID, so renaming doesn't
    break them.

    Args:
        org_id (str):
        secret_id (str):
        body (UpdateSecretRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Secret, UpdateSecretResponse4XX, UpdateSecretResponse5XX]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            secret_id=secret_id,
            client=client,
            body=body,
        )
    ).parsed
