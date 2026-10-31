from typing import Literal, cast

MachineLifecycleState = Literal[
    "active", "delete_failed", "deleted", "deleting", "provision_failed", "provisioning"
]

MACHINE_LIFECYCLE_STATE_VALUES: set[MachineLifecycleState] = {
    "active",
    "delete_failed",
    "deleted",
    "deleting",
    "provision_failed",
    "provisioning",
}


def check_machine_lifecycle_state(value: str) -> MachineLifecycleState:
    if value in MACHINE_LIFECYCLE_STATE_VALUES:
        return cast(MachineLifecycleState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_LIFECYCLE_STATE_VALUES!r}"
    )
