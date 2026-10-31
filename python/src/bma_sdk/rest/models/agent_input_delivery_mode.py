from typing import Literal, cast

AgentInputDeliveryMode = Literal["immediate", "queued", "steering"]

AGENT_INPUT_DELIVERY_MODE_VALUES: set[AgentInputDeliveryMode] = {
    "immediate",
    "queued",
    "steering",
}


def check_agent_input_delivery_mode(value: str) -> AgentInputDeliveryMode:
    if value in AGENT_INPUT_DELIVERY_MODE_VALUES:
        return cast(AgentInputDeliveryMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_INPUT_DELIVERY_MODE_VALUES!r}"
    )
