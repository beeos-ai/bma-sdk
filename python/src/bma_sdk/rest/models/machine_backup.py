import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.machine_backup_reason import (
    MachineBackupReason,
    check_machine_backup_reason,
)
from ..models.machine_backup_state import MachineBackupState, check_machine_backup_state

T = TypeVar("T", bound="MachineBackup")


@_attrs_define
class MachineBackup:
    """
    Attributes:
        id (str):
        machine_id (str): Machine ID (mch_...).
        state (MachineBackupState):
        reason (MachineBackupReason): What took the backup.
        paths (list[str]):
        exclude (list[str]):
        size_bytes (Union[None, int]): Archive size; set once ready.
        digest (Union[None, str]): SHA-256 digest of the tar+zstd archive; set once ready.
        error (str): Why a failed backup failed; empty otherwise.
        created_at (datetime.datetime):
        completed_at (Union[None, datetime.datetime]):
    """

    id: str
    machine_id: str
    state: MachineBackupState
    reason: MachineBackupReason
    paths: list[str]
    exclude: list[str]
    size_bytes: Union[None, int]
    digest: Union[None, str]
    error: str
    created_at: datetime.datetime
    completed_at: Union[None, datetime.datetime]

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        machine_id = self.machine_id

        state: str = self.state

        reason: str = self.reason

        paths = self.paths

        exclude = self.exclude

        size_bytes: Union[None, int]
        size_bytes = self.size_bytes

        digest: Union[None, str]
        digest = self.digest

        error = self.error

        created_at = self.created_at.isoformat()

        completed_at: Union[None, str]
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "machine_id": machine_id,
                "state": state,
                "reason": reason,
                "paths": paths,
                "exclude": exclude,
                "size_bytes": size_bytes,
                "digest": digest,
                "error": error,
                "created_at": created_at,
                "completed_at": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        machine_id = d.pop("machine_id")

        state = check_machine_backup_state(d.pop("state"))

        reason = check_machine_backup_reason(d.pop("reason"))

        paths = cast(list[str], d.pop("paths"))

        exclude = cast(list[str], d.pop("exclude"))

        def _parse_size_bytes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes"))

        def _parse_digest(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        digest = _parse_digest(d.pop("digest"))

        error = d.pop("error")

        created_at = isoparse(d.pop("created_at"))

        def _parse_completed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        machine_backup = cls(
            id=id,
            machine_id=machine_id,
            state=state,
            reason=reason,
            paths=paths,
            exclude=exclude,
            size_bytes=size_bytes,
            digest=digest,
            error=error,
            created_at=created_at,
            completed_at=completed_at,
        )

        return machine_backup
