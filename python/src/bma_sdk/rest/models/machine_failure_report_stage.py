from typing import Literal, cast

MachineFailureReportStage = Literal[
    "daemon_install",
    "daemon_runtime",
    "daemon_uninstall",
    "daemon_uninstalled",
    "daemon_update",
    "startup_script",
]

MACHINE_FAILURE_REPORT_STAGE_VALUES: set[MachineFailureReportStage] = {
    "daemon_install",
    "daemon_runtime",
    "daemon_uninstall",
    "daemon_uninstalled",
    "daemon_update",
    "startup_script",
}


def check_machine_failure_report_stage(value: str) -> MachineFailureReportStage:
    if value in MACHINE_FAILURE_REPORT_STAGE_VALUES:
        return cast(MachineFailureReportStage, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_FAILURE_REPORT_STAGE_VALUES!r}"
    )
