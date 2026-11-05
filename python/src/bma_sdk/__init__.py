"""Python client for the BMA REST API.

    from bma_sdk import Bma

    bma = Bma(token=os.environ["BMA_TOKEN"], base_url=base_url, org_id=org, project_id=project)
    created = bma.agents.sessions.create(agent_id)
    for event in bma.agents.events.stream(agent_id, session_id=created.session.id):
        if event.event == "model_output":
            print(event.data.content_blocks)

Models and request types: :mod:`bma_sdk.types`. BMA extensions to the
Anthropic Managed Agents API: :mod:`bma_sdk.facade_extensions`.
"""

from ._client import DEFAULT_BASE_URL, SDK_VERSION, AsyncBma, Bma
from ._core import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from ._errors import (
    APIConnectionError,
    APIConnectionTimeoutError,
    AuthenticationError,
    BadRequestError,
    BmaApiError,
    BmaError,
    ConflictError,
    ContentTooLargeError,
    ErrorCode,
    EventStreamError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    RequestTimeoutError,
    ServiceUnavailableError,
    UnprocessableEntityError,
)
from ._pagination import AsyncCursorPage, AsyncPaginator, SyncCursorPage
from ._streaming import AsyncStream, Stream
from ._types import NOT_GIVEN, FileTypes, NotGiven
from .lib.tools import AsyncToolRunner, RunnableTool, ToolContext, ToolError, ToolOutput, ToolRunner, define_tool

__version__ = SDK_VERSION
__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "NOT_GIVEN",
    "SDK_VERSION",
    "APIConnectionError",
    "APIConnectionTimeoutError",
    "AsyncBma",
    "AsyncCursorPage",
    "AsyncPaginator",
    "AsyncStream",
    "AsyncToolRunner",
    "AuthenticationError",
    "BadRequestError",
    "Bma",
    "BmaApiError",
    "BmaError",
    "ConflictError",
    "ContentTooLargeError",
    "ErrorCode",
    "EventStreamError",
    "FileTypes",
    "InternalServerError",
    "NotFoundError",
    "NotGiven",
    "PermissionDeniedError",
    "RateLimitError",
    "RequestTimeoutError",
    "RunnableTool",
    "ServiceUnavailableError",
    "Stream",
    "SyncCursorPage",
    "ToolContext",
    "ToolError",
    "ToolOutput",
    "ToolRunner",
    "UnprocessableEntityError",
    "define_tool",
]
