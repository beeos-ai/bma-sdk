"""BMA extension fields on the shared (Claude Managed Agents) objects: top-level
bma_* properties. The official models keep unknown properties in `model_extra`;
the accessors below read them as typed values, and the `*_options` helpers
build the typed `extra_body` of a request to the official method:

    session = client.beta.sessions.create(agent=..., environment_id=...,
        **session_options(model_override={"model": "m1"}, harness={"kind": "acp"}))
    session_extensions(session).model_override

bma_model_override is declared by the contract (x-bma-extension-fields) and
uses its generated types; the other fields follow the facade's current JSON
until the contract lists them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from anthropic import BaseModel
from typing_extensions import NotRequired, TypedDict

from ._generated.models import AgentModelOverride
from ._generated.params import AgentModelOverrideInputParam, AgentModelOverridePatchParam


class Harness(BaseModel):
    """bma_harness: a non-default brain for an agent or a session."""

    kind: str
    agent: Optional[str] = None
    placement: Optional[str] = None
    """Where the environment runs the brain (sessions only)."""


class HarnessParam(TypedDict):
    kind: str
    agent: NotRequired[str]


class EnvironmentWallpaper(BaseModel):
    file_id: str


class EnvironmentDesktop(BaseModel):
    """bma_desktop of an environment: the default wallpaper is a file of the Files API."""

    wallpaper: Optional[EnvironmentWallpaper] = None


class EnvironmentWallpaperParam(TypedDict):
    file_id: str


class EnvironmentDesktopParam(TypedDict):
    wallpaper: Optional[EnvironmentWallpaperParam]


class EnvironmentMachineLease(BaseModel):
    """Who runs on a persistent machine: sessions borrowing it run their turns one at a time."""

    session_id: Optional[str] = None
    queued_sessions: int = 0


class EnvironmentMachine(BaseModel):
    """bma_machine: present on the environment BMA projects from a machine."""

    machine_id: str
    source_kind: str
    lease: EnvironmentMachineLease


@dataclass(frozen=True)
class SessionExt:
    model_override: Optional[AgentModelOverride]
    """The active model override (no key) or None."""
    harness: Optional[Harness]


@dataclass(frozen=True)
class AgentExt:
    harness: Optional[Harness]


@dataclass(frozen=True)
class EnvironmentExt:
    desktop: Optional[EnvironmentDesktop]
    machine: Optional[EnvironmentMachine]


@dataclass(frozen=True)
class EventExt:
    sequence: Optional[int]
    """Orders the events of a session; Last-Event-ID and the history cursor use it (the SSE id stays the opaque event id)."""
    input_id: Optional[str]
    """The BMA input of a user.message."""
    error_code: Optional[str]
    """BMA's reason on a session.error."""


def _raw(obj: Any, name: str) -> Any:
    extra = getattr(obj, "model_extra", None) or {}
    return extra.get(name)


def _model(cls: Any, value: Any) -> Any:
    return None if value is None else cls.construct(**value)


def session_extensions(session: Any) -> SessionExt:
    """The BMA fields of a session returned by client.beta.sessions."""
    return SessionExt(_model(AgentModelOverride, _raw(session, "bma_model_override")), _model(Harness, _raw(session, "bma_harness")))


def agent_extensions(agent: Any) -> AgentExt:
    """The BMA fields of an agent returned by client.beta.agents."""
    return AgentExt(_model(Harness, _raw(agent, "bma_harness")))


def environment_extensions(environment: Any) -> EnvironmentExt:
    """The BMA fields of an environment returned by client.beta.environments."""
    desktop = _raw(environment, "bma_desktop")
    machine = _raw(environment, "bma_machine")
    return EnvironmentExt(
        _model(EnvironmentDesktop, desktop) if desktop is None else EnvironmentDesktop.construct(
            wallpaper=_model(EnvironmentWallpaper, desktop.get("wallpaper"))
        ),
        None if machine is None else EnvironmentMachine.construct(
            machine_id=machine.get("machine_id"),
            source_kind=machine.get("source_kind"),
            lease=EnvironmentMachineLease.construct(**(machine.get("lease") or {})),
        ),
    )


def event_extensions(event: Any) -> EventExt:
    """The BMA fields of a session event: an item of client.beta.sessions.events.list or a frame of stream."""
    return EventExt(_raw(event, "bma_sequence"), _raw(event, "bma_input_id"), _raw(event, "bma_error_code"))


class ExtraBody(TypedDict):
    """Keyword arguments of an official method that carry bma_* request fields."""

    extra_body: Dict[str, object]


_UNSET: Any = object()


def session_options(
    *,
    model_override: Union[AgentModelOverrideInputParam, AgentModelOverridePatchParam, None] = _UNSET,
    harness: HarnessParam = _UNSET,
) -> ExtraBody:
    """Typed bma_* fields for sessions.create / sessions.update.

    `model_override` is an input (sessions.create: lasts for the session;
    sessions.update: replaces the active override), a patch (sessions.update:
    changes fields of it) or None (sessions.update: revokes it). `api_key` is
    write-only. `harness` applies to sessions.create.
    """
    body: Dict[str, object] = {}
    if model_override is not _UNSET:
        body["bma_model_override"] = model_override
    if harness is not _UNSET:
        body["bma_harness"] = harness
    return {"extra_body": body}


def agent_options(*, harness: HarnessParam = _UNSET) -> ExtraBody:
    """Typed bma_harness for agents.create / agents.update."""
    return {"extra_body": {} if harness is _UNSET else {"bma_harness": harness}}


def environment_options(*, desktop: EnvironmentDesktopParam = _UNSET) -> ExtraBody:
    """Typed bma_desktop for environments.create / environments.update."""
    return {"extra_body": {} if desktop is _UNSET else {"bma_desktop": desktop}}
