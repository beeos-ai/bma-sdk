"""Error classes. Names and status mapping follow the TypeScript client and
@anthropic-ai/sdk: one subclass per HTTP status the API documents, plus
connection, timeout and stream errors. ``code`` is the contract's stable error
code (components.schemas.ErrorCode, an x-extensible-enum)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, cast

import httpx
from typing_extensions import TypeAlias

from ._generated.rest.models import AgentConfigErrorIssue
from ._generated.rest.models import ErrorCode as KnownErrorCode
from ._models import construct

__all__ = [
    "APIConnectionError",
    "APIConnectionTimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "BmaApiError",
    "BmaError",
    "ConflictError",
    "ContentTooLargeError",
    "ErrorCode",
    "EventStreamError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "RequestTimeoutError",
    "ServiceUnavailableError",
    "UnprocessableEntityError",
]

ErrorCode: TypeAlias = Union[KnownErrorCode, str]
"""Contract error codes; unknown future codes are still strings."""


class BmaError(Exception):
    """Base class of every error raised by the SDK."""


def _str(value: object) -> Optional[str]:
    return value if isinstance(value, str) and value else None


class BmaApiError(BmaError):
    """An error response from the API, or a request that never got one."""

    status: Optional[int]
    """HTTP status; None for connection errors and stream error frames."""
    headers: Optional[httpx.Headers]
    code: Optional[ErrorCode]
    """Stable error code from the response body."""
    body: object
    """Decoded response body, if any."""
    issues: Optional[List[AgentConfigErrorIssue]]
    """Field-level problems of agent config validation errors."""
    current_digest: Optional[str]
    """Current file digest for file_content_conflict / expected_digest_required."""
    type: Optional[str]
    """Facade extensions only: the Anthropic-style ``error.type``."""

    def __init__(
        self,
        status: Optional[int],
        body: object,
        message: Optional[str] = None,
        headers: Optional[httpx.Headers] = None,
    ) -> None:
        wire = cast(Dict[str, Any], body) if isinstance(body, dict) else {}
        # Native API: {error: string, code}. Facade: {type: "error", error: {type, message, code}}.
        nested = cast(Dict[str, Any], wire["error"]) if isinstance(wire.get("error"), dict) else None
        self.code = _str(nested.get("code") if nested is not None else wire.get("code"))
        self.type = _str(nested.get("type")) if nested is not None else None
        detail = _str(nested.get("message") if nested is not None else wire.get("error")) or message
        self.status = status
        self.headers = headers
        self.body = body
        issues = wire.get("issues")
        self.issues = construct(List[AgentConfigErrorIssue], issues) if isinstance(issues, list) else None
        self.current_digest = _str(wire.get("current_digest"))
        if status is None:
            text = message or detail or "bma: request failed"
        else:
            text = f"bma: {status} {self.code or self.type or 'unknown'}: {detail or f'HTTP {status}'}"
        super().__init__(text)

    @staticmethod
    def generate(status: int, body: object, headers: httpx.Headers) -> "BmaApiError":
        cls = _STATUS_CLASSES.get(status) or (InternalServerError if status >= 500 else BmaApiError)
        return cls(status, body, None, headers)


class APIConnectionError(BmaApiError):
    def __init__(self, message: str = "bma: connection error") -> None:
        super().__init__(None, None, message)


class APIConnectionTimeoutError(APIConnectionError):
    def __init__(self, message: str = "bma: request timed out") -> None:
        super().__init__(message)


class EventStreamError(BmaApiError):
    """An ``error`` frame on an event stream. The stream ends after it; frames
    with code ``service_unavailable`` are retried before this is raised."""

    def __init__(self, body: object) -> None:
        wire = cast(Dict[str, Any], body) if isinstance(body, dict) else {}
        super().__init__(None, body, f"bma: event stream error {wire.get('code', 'unknown')}: {wire.get('error', '')}")


class BadRequestError(BmaApiError):
    pass


class AuthenticationError(BmaApiError):
    pass


class PermissionDeniedError(BmaApiError):
    pass


class NotFoundError(BmaApiError):
    pass


class RequestTimeoutError(BmaApiError):
    pass


class ConflictError(BmaApiError):
    pass


class ContentTooLargeError(BmaApiError):
    pass


class UnprocessableEntityError(BmaApiError):
    pass


class RateLimitError(BmaApiError):
    pass


class InternalServerError(BmaApiError):
    pass


class ServiceUnavailableError(InternalServerError):
    pass


_STATUS_CLASSES: dict[int, type[BmaApiError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    408: RequestTimeoutError,
    409: ConflictError,
    413: ContentTooLargeError,
    422: UnprocessableEntityError,
    429: RateLimitError,
    503: ServiceUnavailableError,
}
