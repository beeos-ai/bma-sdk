from __future__ import annotations

import os
from importlib import metadata
from typing import Any, Mapping, Optional

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import cached_property
from typing_extensions import Self

from ._beta import AsyncBmaBeta, BmaBeta

DEFAULT_BASE_URL = "https://api.bma.beeos.ai"
"""The hosted BMA origin (the paths carry /v1)."""


def _version() -> str:
    try:
        return metadata.version("bma-sdk")
    except metadata.PackageNotFoundError:  # a source checkout that was never installed
        return "0.0.0"


def _settings(
    api_key: Optional[str], base_url: Optional[str], project: Optional[str], default_headers: Optional[Mapping[str, str]], kwargs: dict[str, Any]
) -> dict[str, Any]:
    key = api_key or os.environ.get("BMA_API_KEY", "").strip()
    if not key:
        raise TypeError("set the api_key argument or the BMA_API_KEY environment variable")
    kwargs.pop("auth_token", None)  # copy() passes it; the key is the only credential
    env_project = os.environ.get("BMA_PROJECT_ID", "").strip()
    headers: dict[str, str] = {"X-BMA-SDK": f"bma-sdk-py/{_version()}"}
    if env_project:
        headers["bma-workspace-id"] = env_project
    headers.update(default_headers or {})
    if project:
        headers["bma-workspace-id"] = project
    return {
        **kwargs,
        "api_key": key,
        "base_url": base_url or os.environ.get("BMA_BASE_URL", "").strip() or DEFAULT_BASE_URL,
        "default_headers": headers,
    }


class Bma(Anthropic):
    """The BMA client: the official `anthropic.Anthropic` with the BMA defaults,
    whose `beta` adds the BMA extensions. It never reads ANTHROPIC_API_KEY,
    ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL or the credential profiles of the
    official client: the key defaults to BMA_API_KEY, the origin to BMA_BASE_URL
    and the project (header bma-workspace-id) to BMA_PROJECT_ID.

    Only use it on a server: the API key is a tenant credential. End-user
    clients get single-use tickets instead.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        project: Optional[str] = None,
        default_headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**_settings(api_key, base_url, project, default_headers, kwargs))

    @cached_property
    def beta(self) -> BmaBeta:
        return BmaBeta(self)

    def copy(self, *, project: Optional[str] = None, **kwargs: Any) -> Self:
        """A copy with other options; `project` replaces the project scope."""
        if project:
            kwargs["default_headers"] = {**(kwargs.get("default_headers") or {}), "bma-workspace-id": project}
        return super().copy(**kwargs)

    with_options = copy


class AsyncBma(AsyncAnthropic):
    """The asynchronous BMA client; see `Bma`."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        project: Optional[str] = None,
        default_headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**_settings(api_key, base_url, project, default_headers, kwargs))

    @cached_property
    def beta(self) -> AsyncBmaBeta:
        return AsyncBmaBeta(self)

    def copy(self, *, project: Optional[str] = None, **kwargs: Any) -> Self:
        """A copy with other options; `project` replaces the project scope."""
        if project:
            kwargs["default_headers"] = {**(kwargs.get("default_headers") or {}), "bma-workspace-id": project}
        return super().copy(**kwargs)

    with_options = copy
