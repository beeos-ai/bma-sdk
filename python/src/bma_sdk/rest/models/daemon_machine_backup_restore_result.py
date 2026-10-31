from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.daemon_machine_backup_restore_result_state import (
    DaemonMachineBackupRestoreResultState,
    check_daemon_machine_backup_restore_result_state,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DaemonMachineBackupRestoreResult")


@_attrs_define
class DaemonMachineBackupRestoreResult:
    """
    Attributes:
        state (DaemonMachineBackupRestoreResultState):
        entries (Union[Unset, int]):
        skipped (Union[Unset, int]):
        error (Union[Unset, str]):
    """

    state: DaemonMachineBackupRestoreResultState
    entries: Union[Unset, int] = UNSET
    skipped: Union[Unset, int] = UNSET
    error: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        state: str = self.state

        entries = self.entries

        skipped = self.skipped

        error = self.error

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "state": state,
            }
        )
        if entries is not UNSET:
            field_dict["entries"] = entries
        if skipped is not UNSET:
            field_dict["skipped"] = skipped
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = check_daemon_machine_backup_restore_result_state(d.pop("state"))

        entries = d.pop("entries", UNSET)

        skipped = d.pop("skipped", UNSET)

        error = d.pop("error", UNSET)

        daemon_machine_backup_restore_result = cls(
            state=state,
            entries=entries,
            skipped=skipped,
            error=error,
        )

        return daemon_machine_backup_restore_result
