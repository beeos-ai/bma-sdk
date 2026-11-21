"""Event stream resumption (Last-Event-ID).

A dropped stream reconnects with Last-Event-ID, up to `max_reconnects`
attempts in a row with exponential backoff from `backoff` to `max_backoff`
seconds. One durable BMA event (a `bma_sequence`) projects into several frames
that share its sequence and the server resumes after a whole sequence, so the
reconnect resumes after the previous sequence and skips the frames already
returned: no event is lost or repeated.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Iterator, Optional, Awaitable, AsyncIterator

import anyio
import httpx2
from anthropic import APIConnectionError, APIStatusError
from anthropic._streaming import AsyncStream, Stream

_T = TypeVar("_T")


@dataclass
class ResumeConfig:
    max_reconnects: int = 5
    backoff: float = 0.5
    max_backoff: float = 8.0


CONFIG = ResumeConfig()


class StreamNotResumedError(Exception):
    """The event stream could not be resumed after `max_reconnects` attempts in a row."""


def _retryable(status: int) -> bool:
    return status in (408, 409, 429) or status >= 500


def _position(event: Any) -> tuple[int, str]:
    """The durable position of a frame: its bma_sequence (0 for an ephemeral
    frame such as a delta) and its event id."""
    extra = getattr(event, "model_extra", None) or {}
    seq = extra.get("bma_sequence") or getattr(event, "bma_sequence", 0) or 0
    return int(seq), str(getattr(event, "id", "") or "")


class _Tracker:
    """Which frames were returned already (shared by the sync and async stream)."""

    def __init__(self, after: Optional[int] = None) -> None:
        self.sequence = 0
        self.after = after  # the Last-Event-ID the stream was opened with
        self.seen: set[str] = set()

    def fresh(self, event: Any) -> bool:
        seq, ident = _position(event)
        if seq > 0:
            if seq < self.sequence:
                return False  # replayed after a reconnect
            if seq == self.sequence:
                if ident in self.seen:
                    return False
            else:
                self.sequence = seq
                self.seen.clear()
            self.seen.add(ident)
        elif ident:
            # An announcement ahead of its durable copy (such as the
            # session.status_idle of requires_action): a replay of the current
            # sequence must not return it twice.
            if ident in self.seen:
                return False
            self.seen.add(ident)
        return True

    def resume_id(self) -> Optional[str]:
        # Before any durable frame: the anchor the stream was opened with; None
        # means the server's default position (new events only).
        if self.sequence >= 1:
            return str(self.sequence - 1)
        return None if self.after is None else str(self.after)

    def delay(self, failures: int) -> float:
        return min(CONFIG.backoff * 2**failures, CONFIG.max_backoff)


@dataclass
class _State(Generic[_T]):
    current: Any
    closed: bool = False


class ResumingStream(Stream[_T]):
    """The official `Stream` that reconnects with Last-Event-ID."""

    def __init__(self, first: Stream[_T], connect: Callable[[Optional[str]], Stream[_T]], after: Optional[int] = None) -> None:
        super().__init__(cast_to=first._cast_to, response=first.response, client=first._client, options=first._options)
        self._state: _State[_T] = _State(first)
        self._connect = connect
        self._after = after

    def __stream__(self) -> Iterator[_T]:
        state, track, failures = self._state, _Tracker(self._after), 0
        try:
            while True:
                cause: BaseException = StreamNotResumedError("stream ended")
                try:
                    for event in state.current:
                        if track.fresh(event):
                            failures = 0
                            yield event
                except Exception as err:
                    if state.closed:
                        return
                    if not isinstance(err, (httpx2.TransportError, APIConnectionError)):
                        raise
                    cause = err
                state.current.close()
                while True:
                    if state.closed:
                        return
                    if failures >= CONFIG.max_reconnects:
                        raise StreamNotResumedError(f"event stream not resumed after {failures} attempts") from cause
                    delay = track.delay(failures)
                    failures += 1
                    time.sleep(delay)
                    try:
                        state.current = self._connect(track.resume_id())
                        break
                    except APIStatusError as err:
                        if not _retryable(err.status_code):
                            raise
                        cause = err
                    except APIConnectionError as err:
                        cause = err
        finally:
            state.closed = True
            state.current.close()

    def close(self) -> None:
        self._state.closed = True
        self._state.current.close()


class AsyncResumingStream(AsyncStream[_T]):
    """The official `AsyncStream` that reconnects with Last-Event-ID."""

    def __init__(
        self, first: AsyncStream[_T], connect: Callable[[Optional[str]], Awaitable[AsyncStream[_T]]], after: Optional[int] = None
    ) -> None:
        super().__init__(cast_to=first._cast_to, response=first.response, client=first._client, options=first._options)
        self._state: _State[_T] = _State(first)
        self._connect = connect
        self._after = after

    async def __stream__(self) -> AsyncIterator[_T]:
        state, track, failures = self._state, _Tracker(self._after), 0
        try:
            while True:
                cause: BaseException = StreamNotResumedError("stream ended")
                try:
                    async for event in state.current:
                        if track.fresh(event):
                            failures = 0
                            yield event
                except Exception as err:
                    if state.closed:
                        return
                    if not isinstance(err, (httpx2.TransportError, APIConnectionError)):
                        raise
                    cause = err
                await state.current.close()
                while True:
                    if state.closed:
                        return
                    if failures >= CONFIG.max_reconnects:
                        raise StreamNotResumedError(f"event stream not resumed after {failures} attempts") from cause
                    delay = track.delay(failures)
                    failures += 1
                    await anyio.sleep(delay)
                    try:
                        state.current = await self._connect(track.resume_id())
                        break
                    except APIStatusError as err:
                        if not _retryable(err.status_code):
                            raise
                        cause = err
                    except APIConnectionError as err:
                        cause = err
        finally:
            state.closed = True
            await state.current.close()

    async def close(self) -> None:
        self._state.closed = True
        await self._state.current.close()


def resume_cursor(sent: Any) -> tuple[Optional[int], bool]:
    """The Last-Event-ID for a stream opened after a send, and whether it is a
    replay: the smallest `bma_resume_cursor` of the response's `user.message`
    events; (0, True) when one has none; (None, False) without a `user.message`."""
    after: Optional[int] = None
    for event in getattr(sent, "data", None) or []:
        if getattr(event, "type", None) != "user.message":
            continue
        cursor = (getattr(event, "model_extra", None) or {}).get("bma_resume_cursor")
        if not isinstance(cursor, int) or isinstance(cursor, bool):
            return 0, True
        after = cursor if after is None else min(after, cursor)
    return after, False
