from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DaemonSessionOutput")


@_attrs_define
class DaemonSessionOutput:
    """
    Attributes:
        file_id (str):
        digest (str):
        size_bytes (int):
    """

    file_id: str
    digest: str
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        digest = self.digest

        size_bytes = self.size_bytes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "file_id": file_id,
                "digest": digest,
                "size_bytes": size_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        digest = d.pop("digest")

        size_bytes = d.pop("size_bytes")

        daemon_session_output = cls(
            file_id=file_id,
            digest=digest,
            size_bytes=size_bytes,
        )

        return daemon_session_output
