from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DaemonSessionFile")


@_attrs_define
class DaemonSessionFile:
    """
    Attributes:
        resource_id (str):
        file_id (str):
        mount_path (str): Absolute path below /mnt/session/uploads.
        size_bytes (int):
        digest (str):
    """

    resource_id: str
    file_id: str
    mount_path: str
    size_bytes: int
    digest: str

    def to_dict(self) -> dict[str, Any]:
        resource_id = self.resource_id

        file_id = self.file_id

        mount_path = self.mount_path

        size_bytes = self.size_bytes

        digest = self.digest

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "resource_id": resource_id,
                "file_id": file_id,
                "mount_path": mount_path,
                "size_bytes": size_bytes,
                "digest": digest,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_id = d.pop("resource_id")

        file_id = d.pop("file_id")

        mount_path = d.pop("mount_path")

        size_bytes = d.pop("size_bytes")

        digest = d.pop("digest")

        daemon_session_file = cls(
            resource_id=resource_id,
            file_id=file_id,
            mount_path=mount_path,
            size_bytes=size_bytes,
            digest=digest,
        )

        return daemon_session_file
