"""bma-sdk 2.0: the official Anthropic SDK with the BMA extensions."""
from __future__ import annotations

# The official error classes, so one import serves error handling.
from anthropic import (
    APIError,
    APIStatusError,
    APIConnectionError,
    APITimeoutError,
    AnthropicError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)

from ._beta import AsyncBmaBeta, BmaBeta, SentStream
from ._client import DEFAULT_BASE_URL, AsyncBma, Bma
from ._errors import error_code
from ._extensions import (
    AgentExt,
    EnvironmentDesktop,
    EnvironmentExt,
    EnvironmentMachine,
    EventExt,
    Harness,
    SessionExt,
    agent_extensions,
    agent_options,
    environment_extensions,
    environment_options,
    event_extensions,
    session_extensions,
    session_options,
)
from ._generated import models, params
from ._resume import StreamNotResumedError

__all__ = [
    "APIConnectionError", "APIError", "APIStatusError", "APITimeoutError", "AnthropicError",
    "AsyncBma", "AsyncBmaBeta", "AgentExt", "AuthenticationError", "BadRequestError", "Bma", "BmaBeta",
    "ConflictError", "DEFAULT_BASE_URL", "SentStream", "EnvironmentDesktop", "EnvironmentExt", "EnvironmentMachine",
    "EventExt", "Harness", "InternalServerError", "NotFoundError", "PermissionDeniedError", "RateLimitError",
    "SessionExt", "StreamNotResumedError", "UnprocessableEntityError", "agent_extensions", "agent_options",
    "environment_extensions", "environment_options", "error_code", "event_extensions", "models", "params",
    "session_extensions", "session_options",
]
