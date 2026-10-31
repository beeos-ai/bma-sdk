from typing import Literal, cast

AgentInteractionState = Literal["canceled", "open", "resolved"]

AGENT_INTERACTION_STATE_VALUES: set[AgentInteractionState] = {
    "canceled",
    "open",
    "resolved",
}


def check_agent_interaction_state(value: str) -> AgentInteractionState:
    if value in AGENT_INTERACTION_STATE_VALUES:
        return cast(AgentInteractionState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_INTERACTION_STATE_VALUES!r}"
    )
