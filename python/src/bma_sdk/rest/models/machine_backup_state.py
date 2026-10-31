from typing import Literal, cast

MachineBackupState = Literal["failed", "ready", "uploading"]

MACHINE_BACKUP_STATE_VALUES: set[MachineBackupState] = {
    "failed",
    "ready",
    "uploading",
}


def check_machine_backup_state(value: str) -> MachineBackupState:
    if value in MACHINE_BACKUP_STATE_VALUES:
        return cast(MachineBackupState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_BACKUP_STATE_VALUES!r}"
    )
