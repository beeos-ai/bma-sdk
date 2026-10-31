from typing import Literal, cast

DaemonRuntimeState = Literal["active", "ended"]

DAEMON_RUNTIME_STATE_VALUES: set[DaemonRuntimeState] = {
    "active",
    "ended",
}


def check_daemon_runtime_state(value: str) -> DaemonRuntimeState:
    if value in DAEMON_RUNTIME_STATE_VALUES:
        return cast(DaemonRuntimeState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DAEMON_RUNTIME_STATE_VALUES!r}"
    )
