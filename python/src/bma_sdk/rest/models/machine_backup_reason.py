from typing import Literal, cast

MachineBackupReason = Literal["manual", "pause", "periodic"]

MACHINE_BACKUP_REASON_VALUES: set[MachineBackupReason] = {
    "manual",
    "pause",
    "periodic",
}


def check_machine_backup_reason(value: str) -> MachineBackupReason:
    if value in MACHINE_BACKUP_REASON_VALUES:
        return cast(MachineBackupReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_BACKUP_REASON_VALUES!r}"
    )
