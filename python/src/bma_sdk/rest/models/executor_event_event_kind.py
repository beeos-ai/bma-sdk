from typing import Literal, cast

ExecutorEventEventKind = Literal["executor_event"]

EXECUTOR_EVENT_EVENT_KIND_VALUES: set[ExecutorEventEventKind] = {
    "executor_event",
}


def check_executor_event_event_kind(value: str) -> ExecutorEventEventKind:
    if value in EXECUTOR_EVENT_EVENT_KIND_VALUES:
        return cast(ExecutorEventEventKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EXECUTOR_EVENT_EVENT_KIND_VALUES!r}"
    )
