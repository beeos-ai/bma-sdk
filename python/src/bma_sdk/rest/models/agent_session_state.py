from typing import Literal, cast

AgentSessionState = Literal["active", "archived"]

AGENT_SESSION_STATE_VALUES: set[AgentSessionState] = {
    "active",
    "archived",
}


def check_agent_session_state(value: str) -> AgentSessionState:
    if value in AGENT_SESSION_STATE_VALUES:
        return cast(AgentSessionState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_STATE_VALUES!r}"
    )
