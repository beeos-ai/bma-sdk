from typing import Literal, cast

MachineConnectionState = Literal["asleep", "offline", "online"]

MACHINE_CONNECTION_STATE_VALUES: set[MachineConnectionState] = {
    "asleep",
    "offline",
    "online",
}


def check_machine_connection_state(value: str) -> MachineConnectionState:
    if value in MACHINE_CONNECTION_STATE_VALUES:
        return cast(MachineConnectionState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_CONNECTION_STATE_VALUES!r}"
    )
