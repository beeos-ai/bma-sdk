from typing import Literal, cast

AgentState = Literal["active", "archived"]

AGENT_STATE_VALUES: set[AgentState] = {
    "active",
    "archived",
}


def check_agent_state(value: str) -> AgentState:
    if value in AGENT_STATE_VALUES:
        return cast(AgentState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_STATE_VALUES!r}"
    )
