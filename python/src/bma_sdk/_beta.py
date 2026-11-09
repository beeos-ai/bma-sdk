from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Union

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
from ._resume import AsyncResumingStream, ResumingStream, resume_cursor


@dataclass
class SentStream:
    """The result of `send_and_stream`."""

    sent: Any
    """The send response."""
    stream: Any
    """Starts at the cursor read before the send: its first frames are the sent
    `user.message` and its turn."""
    replayed: bool
    """True when the server gave no `bma_resume_cursor` for a `user.message`: the
    stream replays from `Last-Event-ID: 0`, so it can carry events that precede
    the send; pick this one's turn by `bma_input_id`."""


_SEND_AND_STREAM_DOC = """Send events, then open the resuming stream at the cursor the send returned
        (`bma_resume_cursor`: the session's last sequence before the send), so a
        frame an executor wrote before the stream opened is not lost. The
        official pattern, a stream opened before the send, needs no cursor; this
        one is for a caller that sends first. Without a cursor for a
        `user.message` the stream starts at `Last-Event-ID: 0` (`replayed`); a
        send with no `user.message` streams from the server's default position
        (new events only). A send error raises with no stream; an error opening
        the stream raises too, after the message was accepted."""


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

        return self._open(session_id, None, event_deltas, betas, workspace_id, extra_headers, extra_query, extra_body, timeout)

    def _open(
        self, session_id: str, after: Optional[int], event_deltas: Any, betas: Any, workspace_id: Any,
        extra_headers: Any, extra_query: Any, extra_body: Any, timeout: Any,
    ) -> Stream[BetaManagedAgentsStreamSessionEvents]:
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

        return ResumingStream(open_stream(None if after is None else str(after)), open_stream, after)

    def send_and_stream(
        self,
        session_id: str,
        *,
        events: Any,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SentStream:
        sent = self.send(
            session_id, events=events, betas=betas, workspace_id=workspace_id,
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout,
        )
        after, replayed = resume_cursor(sent)
        stream = self._open(session_id, after, event_deltas, betas, workspace_id, extra_headers, extra_query, extra_body, timeout)
        return SentStream(sent, stream, replayed)

    send_and_stream.__doc__ = _SEND_AND_STREAM_DOC


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

        return await self._open(session_id, None, event_deltas, betas, workspace_id, extra_headers, extra_query, extra_body, timeout)

    async def _open(
        self, session_id: str, after: Optional[int], event_deltas: Any, betas: Any, workspace_id: Any,
        extra_headers: Any, extra_query: Any, extra_body: Any, timeout: Any,
    ) -> AsyncStream[BetaManagedAgentsStreamSessionEvents]:
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

        return AsyncResumingStream(await open_stream(None if after is None else str(after)), open_stream, after)

    async def send_and_stream(
        self,
        session_id: str,
        *,
        events: Any,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SentStream:
        sent = await self.send(
            session_id, events=events, betas=betas, workspace_id=workspace_id,
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout,
        )
        after, replayed = resume_cursor(sent)
        stream = await self._open(session_id, after, event_deltas, betas, workspace_id, extra_headers, extra_query, extra_body, timeout)
        return SentStream(sent, stream, replayed)

    send_and_stream.__doc__ = _SEND_AND_STREAM_DOC


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
