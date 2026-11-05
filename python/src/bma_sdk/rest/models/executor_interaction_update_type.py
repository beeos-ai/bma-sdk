from typing import Literal, cast

ExecutorInteractionUpdateType = Literal["executor_interaction_update"]

EXECUTOR_INTERACTION_UPDATE_TYPE_VALUES: set[ExecutorInteractionUpdateType] = {
    "executor_interaction_update",
}


def check_executor_interaction_update_type(value: str) -> ExecutorInteractionUpdateType:
    if value in EXECUTOR_INTERACTION_UPDATE_TYPE_VALUES:
        return cast(ExecutorInteractionUpdateType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EXECUTOR_INTERACTION_UPDATE_TYPE_VALUES!r}"
    )
