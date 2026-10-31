"""BMA extensions to the Anthropic Managed Agents API.

The standard facade routes (``/v1/agents``, ``/v1/environments``,
``/v1/sessions``, events, events/stream, ``/v1/files``,
``/v1/memory_stores``) are served by the official Anthropic SDKs pointed at a
BMA deployment. Everything in this
package is a BMA extension that is NOT part of the Anthropic contract. The
models and operations under ``_generated`` come from
``contracts/bma/facade-extensions.openapi.yaml``.
"""

from __future__ import annotations

import io
import json
from dataclasses import dataclass
from typing import Any

from ._generated.api.default import (
    add_session_resource,
    delete_session_resource,
    download_session_file,
    get_session_desktop_stream,
    list_session_files,
    list_session_resources,
    upload_session_file,
)
from ._generated.client import Client
from ._generated.models import (
    DeletedSessionResource,
    DesktopStream,
    FileResource,
    FileResourcePage,
    FileResourceParams,
    MCPServerBMAAuth,
    ModelConfigOverride,
    SessionFile,
    SessionFilePage,
    UploadSessionFileBody,
)
from ._generated.types import UNSET, File, Response

__all__ = [
    "IDEMPOTENCY_KEY_HEADER",
    "MAX_SESSION_FILE_BYTES",
    "DeletedSessionResource",
    "DesktopStream",
    "FacadeApiError",
    "FacadeExtensionsClient",
    "FileResource",
    "FileResourcePage",
    "MCPServerBMAAuth",
    "ModelConfigOverride",
    "SessionFile",
    "SessionFileContent",
    "SessionFilePage",
    "bma_sequence",
]

#: BMA extension header forwarded on session create and send-events.
IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"
MAX_SESSION_FILE_BYTES = 8 << 20


class FacadeApiError(Exception):
    """An Anthropic-style error envelope returned by a facade extension route."""

    def __init__(self, status: int, body: Any) -> None:
        error = body.get("error") if isinstance(body, dict) else None
        error = error if isinstance(error, dict) else {}
        self.status = status
        self.type: str = error.get("type") if isinstance(error.get("type"), str) else "api_error"
        self.code: str | None = error.get("code") if isinstance(error.get("code"), str) else None
        self.message: str = error.get("message") or f"HTTP {status}"
        super().__init__(f"bma facade: HTTP {status} {self.type}: {self.message}")


def bma_sequence(event: Any) -> int | None:
    """Return the BMA extension ``bma_sequence`` of a facade session event.

    ``None`` for preview and synthetic events. Send it as ``Last-Event-ID`` to
    resume ``GET /v1/sessions/{id}/events/stream``.
    """
    value = event.get("bma_sequence") if isinstance(event, dict) else None
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else None


@dataclass(frozen=True)
class SessionFileContent:
    """One downloaded session file with its response metadata."""

    content: bytes
    content_type: str | None
    filename: str | None
    digest: str | None


def _disposition_filename(value: str | None) -> str | None:
    if not value:
        return None
    for part in value.split(";"):
        part = part.strip()
        if part.lower().startswith("filename="):
            return part[len("filename="):].strip().strip('"')
    return None


def _check(response: Response[Any]) -> Any:
    status = int(response.status_code)
    if 200 <= status < 300:
        return response.parsed
    try:
        body = json.loads(response.content)
    except ValueError:
        body = None
    raise FacadeApiError(status, body)


class FacadeExtensionsClient:
    """Client for the BMA extension routes of the Anthropic-compatible facade."""

    def __init__(self, api_key: str, base_url: str, *, project_id: str | None = None) -> None:
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError("bma facade: api_key is required")
        base_url = (base_url or "").strip().rstrip("/")
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("bma facade: base_url must be an http or https origin")
        if base_url.endswith("/v1"):
            raise ValueError("bma facade: base_url must be the origin without /v1")
        headers = {"x-api-key": api_key}
        if project_id:
            headers["x-bma-project-id"] = project_id
        self.raw = Client(base_url=base_url, headers=headers)

    def close(self) -> None:
        self.raw.get_httpx_client().close()

    def __enter__(self) -> FacadeExtensionsClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def get_session_desktop_stream(
        self,
        session_id: str,
        *,
        desktop_session_id: str,
        ttl_seconds: int | None = None,
        origin: str | None = None,
    ) -> DesktopStream:
        """BMA extension: ``GET /v1/sessions/{session_id}/desktop/stream``."""
        return _check(
            get_session_desktop_stream.sync_detailed(
                session_id,
                client=self.raw,
                desktop_session_id=desktop_session_id,
                ttl_seconds=UNSET if ttl_seconds is None else ttl_seconds,
                origin=UNSET if origin is None else origin,
            )
        )

    def upload_session_file(self, session_id: str, filename: str, content: bytes) -> SessionFile:
        """BMA extension: ``POST /v1/sessions/{session_id}/files`` (1 byte to 8 MiB)."""
        if not 0 < len(content) <= MAX_SESSION_FILE_BYTES:
            raise ValueError(f"bma facade: session file must be 1..{MAX_SESSION_FILE_BYTES} bytes")
        body = UploadSessionFileBody(file=File(payload=io.BytesIO(content), file_name=filename))
        return _check(upload_session_file.sync_detailed(session_id, client=self.raw, body=body))

    def list_session_files(self, session_id: str, *, limit: int | None = None, page: str | None = None) -> SessionFilePage:
        """BMA extension: ``GET /v1/sessions/{session_id}/files``."""
        return _check(
            list_session_files.sync_detailed(
                session_id,
                client=self.raw,
                limit=UNSET if limit is None else limit,
                page=UNSET if page is None else page,
            )
        )

    def download_session_file(self, session_id: str, file_id: str) -> SessionFileContent:
        """BMA extension: ``GET /v1/sessions/{session_id}/files/{file_id}/content``."""
        response = download_session_file.sync_detailed(session_id, file_id, client=self.raw)
        parsed = _check(response)
        if not isinstance(parsed, File):
            raise FacadeApiError(int(response.status_code), None)
        headers = response.headers
        return SessionFileContent(
            content=parsed.payload.read(),
            content_type=headers.get("content-type"),
            filename=_disposition_filename(headers.get("content-disposition")),
            digest=headers.get("x-bma-file-digest"),
        )

    def add_session_resource(
        self, session_id: str, file_id: str, *, mount_path: str | None = None
    ) -> FileResource:
        """BMA extension: ``POST /v1/sessions/{session_id}/resources``.

        Mounts a project file by reference; the returned ``file_id`` is the
        session instance created for the mount.
        """
        body = FileResourceParams(
            type_="file", file_id=file_id, mount_path=UNSET if mount_path is None else mount_path
        )
        return _check(add_session_resource.sync_detailed(session_id, client=self.raw, body=body))

    def list_session_resources(self, session_id: str) -> FileResourcePage:
        """BMA extension: ``GET /v1/sessions/{session_id}/resources``."""
        return _check(list_session_resources.sync_detailed(session_id, client=self.raw))

    def delete_session_resource(self, session_id: str, resource_id: str) -> DeletedSessionResource:
        """BMA extension: ``DELETE /v1/sessions/{session_id}/resources/{resource_id}``."""
        return _check(delete_session_resource.sync_detailed(session_id, resource_id, client=self.raw))
