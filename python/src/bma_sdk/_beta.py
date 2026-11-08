from __future__ import annotations

from typing import List, Optional, Union

import httpx2
from anthropic._compat import cached_property
from anthropic._streaming import Stream, AsyncStream
from anthropic._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from anthropic.resources.beta import Beta, AsyncBeta
from anthropic.resources.beta.organization import Organization, AsyncOrganization
from anthropic.resources.beta.sessions import Sessions, AsyncSessions
from anthropic.resources.beta.sessions.events import Events, AsyncEvents
from anthropic.types.anthropic_beta_param import AnthropicBetaParam
from anthropic.types.beta.beta_managed_agents_delta_type import BetaManagedAgentsDeltaType
from anthropic.types.beta.sessions.beta_managed_agents_stream_session_events import BetaManagedAgentsStreamSessionEvents

from ._generated.resources import (
    AsyncExtensionServices,
    AsyncOrganizationProjects,
    ExtensionServices,
    OrganizationProjects,
)
from ._resume import AsyncResumingStream, ResumingStream


class BmaEvents(Events):
    """client.beta.sessions.events: the official resource whose `stream` resumes a dropped connection."""

    def stream(
        self,
        session_id: str,
        *,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Stream[BetaManagedAgentsStreamSessionEvents]:
        """Stream Events. Same signature and frames as the official method. When
        the connection drops or the server ends the stream, it reconnects with
        `Last-Event-ID` set to the `bma_sequence` before the one of the last
        frame and returns every event once. The official, non-resuming stream is
        `Events.stream(client.beta.sessions.events, ...)`."""

        def open_stream(last_event_id: Optional[str]) -> Stream[BetaManagedAgentsStreamSessionEvents]:
            headers = extra_headers if last_event_id is None else {**(extra_headers or {}), "Last-Event-ID": last_event_id}
            return Events.stream(
                self,
                session_id,
                event_deltas=event_deltas,
                betas=betas,
                workspace_id=workspace_id,
                extra_headers=headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )

        return ResumingStream(open_stream(None), open_stream)


class AsyncBmaEvents(AsyncEvents):
    """client.beta.sessions.events: the official resource whose `stream` resumes a dropped connection."""

    async def stream(
        self,
        session_id: str,
        *,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[BetaManagedAgentsStreamSessionEvents]:
        """Stream Events. Same signature and frames as the official method, resuming
        a dropped connection with `Last-Event-ID` (see `BmaEvents.stream`)."""

        async def open_stream(last_event_id: Optional[str]) -> AsyncStream[BetaManagedAgentsStreamSessionEvents]:
            headers = extra_headers if last_event_id is None else {**(extra_headers or {}), "Last-Event-ID": last_event_id}
            return await AsyncEvents.stream(
                self,
                session_id,
                event_deltas=event_deltas,
                betas=betas,
                workspace_id=workspace_id,
                extra_headers=headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )

        return AsyncResumingStream(await open_stream(None), open_stream)


class BmaSessions(Sessions):
    @cached_property
    def events(self) -> BmaEvents:
        return BmaEvents(self._client)


class AsyncBmaSessions(AsyncSessions):
    @cached_property
    def events(self) -> AsyncBmaEvents:
        return AsyncBmaEvents(self._client)


class BmaOrganization(Organization):
    """client.beta.organization: the official resource plus `projects`."""

    @cached_property
    def projects(self) -> OrganizationProjects:
        return OrganizationProjects(self._client)


class AsyncBmaOrganization(AsyncOrganization):
    """client.beta.organization: the official resource plus `projects`."""

    @cached_property
    def projects(self) -> AsyncOrganizationProjects:
        return AsyncOrganizationProjects(self._client)


class BmaBeta(Beta):
    """client.beta: the official Beta resources plus the BMA extensions."""

    @cached_property
    def sessions(self) -> BmaSessions:
        return BmaSessions(self._client)

    @cached_property
    def organization(self) -> BmaOrganization:
        return BmaOrganization(self._client)

    @cached_property
    def _extensions(self) -> ExtensionServices:
        return ExtensionServices(self._client)

    @property
    def machines(self):
        return self._extensions.machines

    @property
    def machine_pools(self):
        return self._extensions.machine_pools

    @property
    def desktop_sessions(self):
        return self._extensions.desktop_sessions

    @property
    def terminal_sessions(self):
        return self._extensions.terminal_sessions


class AsyncBmaBeta(AsyncBeta):
    """client.beta: the official Beta resources plus the BMA extensions."""

    @cached_property
    def sessions(self) -> AsyncBmaSessions:
        return AsyncBmaSessions(self._client)

    @cached_property
    def organization(self) -> AsyncBmaOrganization:
        return AsyncBmaOrganization(self._client)

    @cached_property
    def _extensions(self) -> AsyncExtensionServices:
        return AsyncExtensionServices(self._client)

    @property
    def machines(self):
        return self._extensions.machines

    @property
    def machine_pools(self):
        return self._extensions.machine_pools

    @property
    def desktop_sessions(self):
        return self._extensions.desktop_sessions

    @property
    def terminal_sessions(self):
        return self._extensions.terminal_sessions
