from typing import Literal, cast

CreateAgentInputDeliveryMode = Literal["queued", "steering"]

CREATE_AGENT_INPUT_DELIVERY_MODE_VALUES: set[CreateAgentInputDeliveryMode] = {
    "queued",
    "steering",
}


def check_create_agent_input_delivery_mode(value: str) -> CreateAgentInputDeliveryMode:
    if value in CREATE_AGENT_INPUT_DELIVERY_MODE_VALUES:
        return cast(CreateAgentInputDeliveryMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_AGENT_INPUT_DELIVERY_MODE_VALUES!r}"
    )
