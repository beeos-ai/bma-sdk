from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DaemonMachineBackupArchive")


@_attrs_define
class DaemonMachineBackupArchive:
    """
    Attributes:
        digest (str):
        size_bytes (int):
    """

    digest: str
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        digest = self.digest

        size_bytes = self.size_bytes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "digest": digest,
                "size_bytes": size_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        digest = d.pop("digest")

        size_bytes = d.pop("size_bytes")

        daemon_machine_backup_archive = cls(
            digest=digest,
            size_bytes=size_bytes,
        )

        return daemon_machine_backup_archive
