from typing import Literal, cast

AgentControlType = Literal["cancel_current"]

AGENT_CONTROL_TYPE_VALUES: set[AgentControlType] = {
    "cancel_current",
}


def check_agent_control_type(value: str) -> AgentControlType:
    if value in AGENT_CONTROL_TYPE_VALUES:
        return cast(AgentControlType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONTROL_TYPE_VALUES!r}"
    )
