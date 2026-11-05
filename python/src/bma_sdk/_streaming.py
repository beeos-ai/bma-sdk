"""Server-sent event streams."""

from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator, Callable, Generic, Iterator, List, Optional, TypeVar

from typing_extensions import Self

from ._errors import BmaError

T = TypeVar("T")

__all__ = ["AsyncStream", "Stream"]


class Stream(Generic[T]):
    """A typed event stream. Iterate it once; ``close()`` (or leaving a
    ``with`` block) closes the connection. Like EventSource, the stream does
    not end when the server closes the connection: it reconnects from the last
    durable frame until the reconnect budget is spent, then raises."""

    def __init__(self, iterate: Callable[[], Iterator[T]], close: Callable[[], object]) -> None:
        self._iterate = iterate
        self._close = close
        self._iterator: Optional[Iterator[T]] = None
        self.closed: bool = False

    def __iter__(self) -> Iterator[T]:
        if self._iterator is not None:
            raise BmaError("bma: a Stream can be iterated only once")
        self._iterator = self._iterate()
        return self._iterator

    def close(self) -> None:
        """Closes the connection; safe to call from another thread."""
        self.closed = True
        self._close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class AsyncStream(Generic[T]):
    """A typed event stream. Iterate it once with ``async for``; ``close()``
    (or leaving an ``async with`` block) closes the connection."""

    def __init__(self, iterate: Callable[[], AsyncIterator[T]]) -> None:
        self._iterate = iterate
        self._iterator: Optional[AsyncIterator[T]] = None

    def __aiter__(self) -> AsyncIterator[T]:
        if self._iterator is not None:
            raise BmaError("bma: an AsyncStream can be iterated only once")
        self._iterator = self._iterate()
        return self._iterator

    async def close(self) -> None:
        if self._iterator is not None:
            await self._iterator.aclose()  # type: ignore[attr-defined]

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()


@dataclass
class RawFrame:
    event: str
    id: Optional[str]
    data: str


class _Parser:
    """Minimal text/event-stream parser (WHATWG SSE field rules)."""

    def __init__(self) -> None:
        self.event = ""
        self.id: Optional[str] = None
        self.data: List[str] = []

    def line(self, line: str) -> Optional[RawFrame]:
        if line == "":
            return self.dispatch()
        if line.startswith(":"):
            return None
        name, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if name == "event":
            self.event = value
        elif name == "id":
            self.id = value
        elif name == "data":
            self.data.append(value)
        return None

    def dispatch(self) -> Optional[RawFrame]:
        frame = RawFrame(self.event or "message", self.id, "\n".join(self.data)) if self.data else None
        self.event, self.id, self.data = "", None, []
        return frame


def iter_sse(lines: Iterator[str], on_line: Optional[Callable[[], object]] = None) -> Iterator[RawFrame]:
    """Frames of an event stream. A frame not terminated by a blank line when
    the body ends is discarded (WHATWG HTML §9.2.6). ``on_line`` runs for
    every line, comments (heartbeats) included."""
    parser = _Parser()
    for line in lines:
        if on_line is not None:
            on_line()
        frame = parser.line(line)
        if frame is not None:
            yield frame


async def aiter_sse(lines: AsyncIterator[str], on_line: Optional[Callable[[], object]] = None) -> AsyncIterator[RawFrame]:
    parser = _Parser()
    async for line in lines:
        if on_line is not None:
            on_line()
        frame = parser.line(line)
        if frame is not None:
            yield frame
