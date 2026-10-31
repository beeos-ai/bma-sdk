from typing import Literal, cast

CronTriggerLastRunState = Literal["completed", "failed", "processing", "queued"]

CRON_TRIGGER_LAST_RUN_STATE_VALUES: set[CronTriggerLastRunState] = {
    "completed",
    "failed",
    "processing",
    "queued",
}


def check_cron_trigger_last_run_state(value: str) -> CronTriggerLastRunState:
    if value in CRON_TRIGGER_LAST_RUN_STATE_VALUES:
        return cast(CronTriggerLastRunState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CRON_TRIGGER_LAST_RUN_STATE_VALUES!r}"
    )
