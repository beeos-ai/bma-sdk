from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._core import AsyncClientCore, SyncClientCore

__all__ = ["AsyncAPIResource", "SyncAPIResource"]


class SyncAPIResource:
    def __init__(self, client: "SyncClientCore") -> None:
        self._client = client


class AsyncAPIResource:
    def __init__(self, client: "AsyncClientCore") -> None:
        self._client = client
