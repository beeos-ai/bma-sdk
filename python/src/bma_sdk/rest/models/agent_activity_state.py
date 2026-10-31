from typing import Literal, cast

AgentActivityState = Literal["archived", "idle", "running", "waiting_on_interaction"]

AGENT_ACTIVITY_STATE_VALUES: set[AgentActivityState] = {
    "archived",
    "idle",
    "running",
    "waiting_on_interaction",
}


def check_agent_activity_state(value: str) -> AgentActivityState:
    if value in AGENT_ACTIVITY_STATE_VALUES:
        return cast(AgentActivityState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_ACTIVITY_STATE_VALUES!r}"
    )
