from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

T = TypeVar("T", bound="DaemonMachineBackupRestore")


@_attrs_define
class DaemonMachineBackupRestore:
    """
    Attributes:
        backup_id (str):
        digest (str):
        size_bytes (int):
        paths (list[str]):
    """

    backup_id: str
    digest: str
    size_bytes: int
    paths: list[str]

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        digest = self.digest

        size_bytes = self.size_bytes

        paths = self.paths

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "backup_id": backup_id,
                "digest": digest,
                "size_bytes": size_bytes,
                "paths": paths,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backup_id = d.pop("backup_id")

        digest = d.pop("digest")

        size_bytes = d.pop("size_bytes")

        paths = cast(list[str], d.pop("paths"))

        daemon_machine_backup_restore = cls(
            backup_id=backup_id,
            digest=digest,
            size_bytes=size_bytes,
            paths=paths,
        )

        return daemon_machine_backup_restore
