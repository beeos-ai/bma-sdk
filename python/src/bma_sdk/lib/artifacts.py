"""agents.artifacts.download: artifact content verified against the size and
sha256 digest recorded on the artifact."""

from __future__ import annotations

import hashlib
import hmac
import re
from typing import Optional

from .._core import RequestOptions
from .._errors import BmaError
from .._generated.rest import operations as _ops
from .._generated.rest.models import Artifact
from .._resource import AsyncAPIResource, SyncAPIResource
from .._types import NOT_GIVEN, NotGiven

__all__ = ["ArtifactsBase", "AsyncArtifactsBase"]

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _check(artifact: Artifact, max_bytes: int) -> int:
    size: Optional[int] = getattr(artifact, "size_bytes", None)
    if max_bytes <= 0:
        raise BmaError("bma: max_bytes is required")
    if not isinstance(size, int) or size < 0 or size > max_bytes:
        raise BmaError("bma: artifact size is missing or exceeds max_bytes")
    if not _DIGEST.match(getattr(artifact, "digest", None) or ""):
        raise BmaError("bma: artifact digest must be sha256:<hex>")
    return size


def _verify(artifact: Artifact, size: int, chunks: list[bytes]) -> bytes:
    data = b"".join(chunks)
    if len(data) != size:
        raise BmaError(f"bma: artifact size = {len(data)}, want {size}")
    if not hmac.compare_digest("sha256:" + hashlib.sha256(data).hexdigest(), artifact.digest or ""):
        raise BmaError("bma: artifact digest mismatch")
    return data


def _path(artifact: Artifact) -> dict[str, str]:
    return {"orgID": artifact.org_id, "projectID": artifact.project_id, "agentID": artifact.agent_id, "artifactID": artifact.id}


class ArtifactsBase(SyncAPIResource):
    def download(self, artifact: Artifact, *, max_bytes: int, timeout: float | NotGiven = NOT_GIVEN) -> bytes:
        """Downloads artifact content and verifies its size and sha256 digest.
        The body is buffered, bounded by ``max_bytes``."""
        size = _check(artifact, max_bytes)
        chunks: list[bytes] = []
        total = 0
        response = self._client._open(_ops.getArtifactContent, _path(artifact), {}, RequestOptions(timeout=timeout))
        try:
            for chunk in response.iter_bytes():
                total += len(chunk)
                if total > size:
                    raise BmaError(f"bma: artifact is larger than {size} bytes")
                chunks.append(chunk)
        finally:
            response.close()
        return _verify(artifact, size, chunks)


class AsyncArtifactsBase(AsyncAPIResource):
    async def download(self, artifact: Artifact, *, max_bytes: int, timeout: float | NotGiven = NOT_GIVEN) -> bytes:
        size = _check(artifact, max_bytes)
        chunks: list[bytes] = []
        total = 0
        response = await self._client._open(_ops.getArtifactContent, _path(artifact), {}, RequestOptions(timeout=timeout))
        try:
            async for chunk in response.aiter_bytes():
                total += len(chunk)
                if total > size:
                    raise BmaError(f"bma: artifact is larger than {size} bytes")
                chunks.append(chunk)
        finally:
            await response.aclose()
        return _verify(artifact, size, chunks)
