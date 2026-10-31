from typing import Literal, cast

DesktopControlStatusMode = Literal["agent", "human", "paused"]

DESKTOP_CONTROL_STATUS_MODE_VALUES: set[DesktopControlStatusMode] = {
    "agent",
    "human",
    "paused",
}


def check_desktop_control_status_mode(value: str) -> DesktopControlStatusMode:
    if value in DESKTOP_CONTROL_STATUS_MODE_VALUES:
        return cast(DesktopControlStatusMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DESKTOP_CONTROL_STATUS_MODE_VALUES!r}"
    )
