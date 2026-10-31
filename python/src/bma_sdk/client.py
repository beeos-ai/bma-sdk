"""Authenticated BMA REST client.

Every operation and model lives in :mod:`bma_sdk.rest`, generated from
``contracts/bma/rest.openapi.yaml``. This module adds only what the contract
does not describe: bearer authentication, error decoding, the server-sent
event stream, and verified artifact downloads.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

import httpx

from .rest.client import AuthenticatedClient
from .rest.models.artifact import Artifact
from .rest.types import Response

DEFAULT_BASE_URL = "https://api.bma.beeos.ai/v1"
SDK_VERSION = "0.4.0"
_USER_AGENT = f"bma-sdks-python/{SDK_VERSION}"
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class BmaApiError(Exception):
    """A non-2xx response from the BMA API."""

    def __init__(self, status: int, body: Any) -> None:
        wire = body if isinstance(body, dict) else {}
        self.status = status
        self.code: str = wire.get("code") if isinstance(wire.get("code"), str) else ""
        message = wire.get("error") if isinstance(wire.get("error"), str) and wire.get("error") else f"HTTP {status}"
        self.message: str = message
        self.current_digest: str | None = wire.get("current_digest")
        self.issues: list[Any] | None = wire.get("issues")
        super().__init__(f"bma: HTTP {status} {self.code or 'unknown'}: {message}")

    @property
    def retryable(self) -> bool:
        """Whether a retry may succeed without changing the request."""
        return (
            self.status in (408, 429)
            or self.status >= 500
            or self.code in ("service_unavailable", "rate_limited")
        )


def unwrap(response: Response[Any]) -> Any:
    """Return ``response.parsed`` for 2xx responses or raise :class:`BmaApiError`.

    Use with the generated ``sync_detailed``/``asyncio_detailed`` functions.
    """
    status = int(response.status_code)
    if 200 <= status < 300:
        return response.parsed
    try:
        body = json.loads(response.content)
    except ValueError:
        body = None
    raise BmaApiError(status, body)


@dataclass(frozen=True)
class StreamFrame:
    """One SSE data frame. ``data`` is the decoded JSON payload."""

    event: str
    data: Any
    id: str | None = None
    sequence: int | None = None


class BmaClient:
    """BMA REST client.

    ``client.rest`` is the generated :class:`bma_sdk.rest.client.AuthenticatedClient`
    to pass to any generated operation, for example::

        from bma_sdk.rest.api.agents import create_agent_session
        session = unwrap(create_agent_session.sync_detailed(org, project, agent, client=bma.rest, body=...))
    """

    def __init__(self, token: str, base_url: str = DEFAULT_BASE_URL) -> None:
        token = (token or "").strip()
        if not token:
            raise ValueError("bma: token is required")
        base_url = (base_url or DEFAULT_BASE_URL).strip().rstrip("/")
        if urlsplit(base_url).scheme not in ("http", "https"):
            raise ValueError("bma: base_url must use http or https")
        self.base_url = base_url
        self.rest = AuthenticatedClient(base_url=base_url, token=token, headers={"User-Agent": _USER_AGENT})

    def close(self) -> None:
        self.rest.get_httpx_client().close()

    def __enter__(self) -> BmaClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def stream_events(
        self,
        org_id: str,
        project_id: str,
        agent_id: str,
        *,
        session_id: str | None = None,
        after_sequence: int | None = None,
        last_event_id: int | None = None,
        stream_deltas: bool | None = None,
    ) -> Iterator[StreamFrame]:
        """Iterate ``GET .../agents/{agent_id}/events/stream``.

        Heartbeat comments are skipped; the iterator ends when the server closes
        the stream.
        """
        params: dict[str, str] = {}
        if session_id is not None:
            params["session_id"] = session_id
        if after_sequence is not None:
            params["after_sequence"] = str(after_sequence)
        if stream_deltas is not None:
            params["stream_deltas"] = "true" if stream_deltas else "false"
        headers = {"Accept": "text/event-stream"}
        if last_event_id is not None:
            headers["Last-Event-ID"] = str(last_event_id)
        path = f"/orgs/{org_id}/projects/{project_id}/agents/{agent_id}/events/stream"
        with self.rest.get_httpx_client().stream("GET", path, params=params, headers=headers, timeout=None) as response:
            _raise_for_status(response)
            media = response.headers.get("content-type", "").split(";")[0].strip()
            if media != "text/event-stream":
                raise ValueError(f"bma: event stream content type = {media!r}")
            for event, frame_id, data in parse_sse(response.iter_lines()):
                sequence = None
                if frame_id is not None:
                    if not frame_id.isdigit():
                        raise ValueError(f"bma: invalid event id {frame_id!r}")
                    sequence = int(frame_id)
                yield StreamFrame(event=event, data=json.loads(data), id=frame_id, sequence=sequence)

    def download_artifact(self, artifact: Artifact, *, max_bytes: int) -> bytes:
        """Download artifact content and verify its recorded size and sha256 digest."""
        size = artifact.size_bytes
        if max_bytes <= 0:
            raise ValueError("bma: max_bytes is required")
        if not isinstance(size, int) or size < 0 or size > max_bytes:
            raise ValueError("bma: artifact size is missing or exceeds max_bytes")
        digest = artifact.digest if isinstance(artifact.digest, str) else ""
        if not _DIGEST.match(digest):
            raise ValueError("bma: artifact digest must be sha256:<hex>")
        path = (
            f"/orgs/{artifact.org_id}/projects/{artifact.project_id}"
            f"/agents/{artifact.agent_id}/artifacts/{artifact.id}/content"
        )
        hasher = hashlib.sha256()
        chunks: list[bytes] = []
        total = 0
        with self.rest.get_httpx_client().stream(
            "GET", path, headers={"Accept": "application/octet-stream"}
        ) as response:
            _raise_for_status(response)
            for chunk in response.iter_bytes():
                total += len(chunk)
                if total > size:
                    raise ValueError(f"bma: artifact is larger than {size} bytes")
                hasher.update(chunk)
                chunks.append(chunk)
        if total != size:
            raise ValueError(f"bma: artifact size = {total}, want {size}")
        if not hmac.compare_digest("sha256:" + hasher.hexdigest(), digest):
            raise ValueError("bma: artifact digest mismatch")
        return b"".join(chunks)


def _raise_for_status(response: httpx.Response) -> None:
    if 200 <= response.status_code < 300:
        return
    raw = response.read()
    try:
        body = json.loads(raw)
    except ValueError:
        body = None
    raise BmaApiError(response.status_code, body)


def parse_sse(lines: Iterator[str]) -> Iterator[tuple[str, str | None, str]]:
    """Minimal text/event-stream parser yielding ``(event, id, data)``."""
    event, frame_id, data = "", None, []
    for line in lines:
        if line == "":
            if data:
                yield event or "message", frame_id, "\n".join(data)
            event, frame_id, data = "", None, []
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        value = value[1:] if value.startswith(" ") else value
        if field == "event":
            event = value
        elif field == "id":
            frame_id = value
        elif field == "data":
            data.append(value)
    if data:
        yield event or "message", frame_id, "\n".join(data)
