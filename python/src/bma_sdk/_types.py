"""Shared argument types of the resource methods."""

from __future__ import annotations

from typing import IO, Mapping, Tuple, Union

from typing_extensions import Literal, TypeAlias, final


@final
class NotGiven:
    """Sentinel for an omitted keyword argument, so that ``None`` can still
    send JSON ``null`` (the Stainless SDKs' ``NOT_GIVEN``)."""

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()

FileContent: TypeAlias = Union[bytes, IO[bytes]]
FileTypes: TypeAlias = Union[
    FileContent,
    Tuple[str, FileContent],
    Tuple[str, FileContent, str],
]
"""A multipart file: content, ``(filename, content)`` or ``(filename, content, content_type)``."""

Headers: TypeAlias = Mapping[str, str]
Query: TypeAlias = Mapping[str, object]
