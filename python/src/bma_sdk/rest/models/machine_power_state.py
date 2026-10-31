from typing import Literal, cast

MachinePowerState = Literal[
    "archived", "archiving", "paused", "pausing", "resuming", "running"
]

MACHINE_POWER_STATE_VALUES: set[MachinePowerState] = {
    "archived",
    "archiving",
    "paused",
    "pausing",
    "resuming",
    "running",
}


def check_machine_power_state(value: str) -> MachinePowerState:
    if value in MACHINE_POWER_STATE_VALUES:
        return cast(MachinePowerState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_POWER_STATE_VALUES!r}"
    )
