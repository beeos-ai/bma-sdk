import datetime
from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="SessionFile")


@_attrs_define
class SessionFile:
    """
    Attributes:
        id (str): Opaque, stable file id.
        type_ (Literal['file']):
        filename (str):
        mime_type (str): Derived from the filename extension; advisory.
        size_bytes (int):
        created_at (datetime.datetime):
    """

    id: str
    type_: Literal["file"]
    filename: str
    mime_type: str
    size_bytes: int
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        filename = self.filename

        mime_type = self.mime_type

        size_bytes = self.size_bytes

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "filename": filename,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["file"], d.pop("type"))
        if type_ != "file":
            raise ValueError(f"type must match const 'file', got '{type_}'")

        filename = d.pop("filename")

        mime_type = d.pop("mime_type")

        size_bytes = d.pop("size_bytes")

        created_at = isoparse(d.pop("created_at"))

        session_file = cls(
            id=id,
            type_=type_,
            filename=filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            created_at=created_at,
        )

        return session_file
