from typing import Literal, cast

IntegrationState = Literal["active", "disconnected"]

INTEGRATION_STATE_VALUES: set[IntegrationState] = {
    "active",
    "disconnected",
}


def check_integration_state(value: str) -> IntegrationState:
    if value in INTEGRATION_STATE_VALUES:
        return cast(IntegrationState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INTEGRATION_STATE_VALUES!r}"
    )
