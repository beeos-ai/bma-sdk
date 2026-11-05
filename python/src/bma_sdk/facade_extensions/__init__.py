"""BMA extensions to the Anthropic Managed Agents API.

The standard facade routes (``/v1/agents``, ``/v1/environments``,
``/v1/sessions``, events, events/stream, ``/v1/files``,
``/v1/memory_stores``) are served by the official Anthropic SDKs pointed at a
BMA deployment. This package covers only the BMA extensions, as resources::

    ext = FacadeExtensions(api_key=api_key, base_url="https://api.bma.beeos.ai", project_id=project)
    ext.sessions.files.list(session_id)

Resource classes are generated from contracts/bma/facade-extensions.openapi.yaml
and the ``facade`` section of contracts/bma/sdk.resources.yaml; models and
request types are in :mod:`bma_sdk.facade_extensions.types`.
"""

from __future__ import annotations

from typing import Dict, Mapping, Optional

import httpx
from typing_extensions import Self

from .._core import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from .._errors import BmaError
from .._generated.facade.resources import AsyncFacadeClientBase, FacadeClientBase

__all__ = ["AsyncFacadeExtensions", "FacadeExtensions", "bma_sequence"]


def bma_sequence(event: object) -> Optional[int]:
    """The BMA extension ``bma_sequence`` of a facade session event (a dict or
    an Anthropic SDK event object), or ``None`` for preview and synthetic
    events. Send it as ``Last-Event-ID`` to resume
    ``GET /v1/sessions/{id}/events/stream``."""
    value = event.get("bma_sequence") if isinstance(event, Mapping) else getattr(event, "bma_sequence", None)
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else None


def _options(api_key: str, base_url: str, project_id: Optional[str]) -> Dict[str, object]:
    api_key = (api_key or "").strip()
    if not api_key:
        raise BmaError("bma facade: api_key is required")
    base_url = (base_url or "").strip().rstrip("/")
    if not base_url:
        raise BmaError("bma facade: base_url is required")
    if base_url.endswith("/v1"):
        raise BmaError("bma facade: base_url must be the origin without /v1")
    return {
        "base_url": base_url,
        "headers": {"x-api-key": api_key},
        "scope": {"project_id": project_id},
        "scope_option": {"project_id": "project_id"},
    }


class FacadeExtensions(FacadeClientBase):
    """Client for the BMA extension routes of the Anthropic-compatible facade.

    ``api_key`` is a BMA organization API key (sent as ``x-api-key``);
    ``base_url`` the facade origin without ``/v1``; ``project_id`` the default
    ``x-bma-project-id`` (required for multi-project keys)."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        project_id: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(
            http_client=http_client, timeout=timeout, max_retries=max_retries,
            **_options(api_key, base_url, project_id),
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class AsyncFacadeExtensions(AsyncFacadeClientBase):
    """Asynchronous :class:`FacadeExtensions`."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        project_id: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(
            http_client=http_client, timeout=timeout, max_retries=max_retries,
            **_options(api_key, base_url, project_id),
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()
