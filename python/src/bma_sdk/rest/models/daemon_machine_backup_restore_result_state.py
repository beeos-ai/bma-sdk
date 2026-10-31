from typing import Literal, cast

DaemonMachineBackupRestoreResultState = Literal["failed", "restored"]

DAEMON_MACHINE_BACKUP_RESTORE_RESULT_STATE_VALUES: set[
    DaemonMachineBackupRestoreResultState
] = {
    "failed",
    "restored",
}


def check_daemon_machine_backup_restore_result_state(
    value: str,
) -> DaemonMachineBackupRestoreResultState:
    if value in DAEMON_MACHINE_BACKUP_RESTORE_RESULT_STATE_VALUES:
        return cast(DaemonMachineBackupRestoreResultState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DAEMON_MACHINE_BACKUP_RESTORE_RESULT_STATE_VALUES!r}"
    )
