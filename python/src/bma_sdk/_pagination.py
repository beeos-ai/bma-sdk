"""Cursor pagination, after the Stainless ``SyncCursorPage``/``AsyncPaginator``
of the Anthropic Python SDK: a sync list method returns the first page, and
iterating it walks every item across pages; an async list method returns a
paginator that is awaitable (first page) and async-iterable (every item).
Applies to every list whose response is ``{data: [...], next_<param>}`` for a
query parameter <param> (``cursor``, ``page``, ``before_id``/``after_id``,
``before_sequence``/``after_sequence``); ``next_cursor`` is the value the next
request sends in that parameter."""

from __future__ import annotations

from typing import Any, AsyncIterator, Awaitable, Callable, Generator, Generic, Iterator, List, Optional, TypeVar, Union

from ._errors import BmaError

T = TypeVar("T")

__all__ = ["AsyncCursorPage", "AsyncPaginator", "SyncCursorPage"]


class SyncCursorPage(Generic[T]):
    def __init__(self, data: List[T], next_cursor: Optional[Union[str, int]], fetch: Callable[[Any], "SyncCursorPage[T]"]) -> None:
        self.data = data
        self.next_cursor = next_cursor
        self._fetch = fetch

    def has_next_page(self) -> bool:
        return self.next_cursor is not None and len(self.data) > 0

    def get_next_page(self) -> "SyncCursorPage[T]":
        """Fetches the next page; raises when there is none."""
        if not self.has_next_page() or self.next_cursor is None:
            raise BmaError("bma: no next page; check has_next_page() first")
        return self._fetch(self.next_cursor)

    def iter_pages(self) -> Iterator["SyncCursorPage[T]"]:
        """This page and every following page."""
        page = self
        yield page
        while page.has_next_page():
            page = page.get_next_page()
            yield page

    def __iter__(self) -> Iterator[T]:
        """Every item of this page and every following page."""
        for page in self.iter_pages():
            yield from page.data


class AsyncCursorPage(Generic[T]):
    def __init__(
        self, data: List[T], next_cursor: Optional[Union[str, int]], fetch: Callable[[Any], Awaitable["AsyncCursorPage[T]"]]
    ) -> None:
        self.data = data
        self.next_cursor = next_cursor
        self._fetch = fetch

    def has_next_page(self) -> bool:
        return self.next_cursor is not None and len(self.data) > 0

    async def get_next_page(self) -> "AsyncCursorPage[T]":
        if not self.has_next_page() or self.next_cursor is None:
            raise BmaError("bma: no next page; check has_next_page() first")
        return await self._fetch(self.next_cursor)

    async def iter_pages(self) -> AsyncIterator["AsyncCursorPage[T]"]:
        page = self
        yield page
        while page.has_next_page():
            page = await page.get_next_page()
            yield page

    async def __aiter__(self) -> AsyncIterator[T]:
        async for page in self.iter_pages():
            for item in page.data:
                yield item


class AsyncPaginator(Generic[T]):
    """``await`` for the first page, ``async for`` for every item."""

    def __init__(self, fetch: Callable[[Any], Awaitable[AsyncCursorPage[T]]]) -> None:
        self._fetch = fetch

    def __await__(self) -> Generator[object, None, AsyncCursorPage[T]]:
        return self._fetch(None).__await__()

    async def __aiter__(self) -> AsyncIterator[T]:
        page = await self._fetch(None)
        async for item in page:
            yield item
