"""Response models (pydantic) and request types (TypedDict, ``*Param``) of
the BMA REST API, generated from contracts/bma/rest.openapi.yaml."""

from typing_extensions import TypeAlias

from .._generated.rest.models import *  # noqa: F403
from .._generated.rest.models import StreamEventsEvent
from .._generated.rest.params import *  # noqa: F403

AgentStreamEvent: TypeAlias = StreamEventsEvent
"""One frame of ``agents.events.stream``, discriminated by ``event``."""
