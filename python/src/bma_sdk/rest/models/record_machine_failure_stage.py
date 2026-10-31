from typing import Literal, cast

RecordMachineFailureStage = Literal[
    "daemon_install",
    "daemon_runtime",
    "daemon_uninstall",
    "daemon_uninstalled",
    "daemon_update",
    "startup_script",
]

RECORD_MACHINE_FAILURE_STAGE_VALUES: set[RecordMachineFailureStage] = {
    "daemon_install",
    "daemon_runtime",
    "daemon_uninstall",
    "daemon_uninstalled",
    "daemon_update",
    "startup_script",
}


def check_record_machine_failure_stage(value: str) -> RecordMachineFailureStage:
    if value in RECORD_MACHINE_FAILURE_STAGE_VALUES:
        return cast(RecordMachineFailureStage, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {RECORD_MACHINE_FAILURE_STAGE_VALUES!r}"
    )
