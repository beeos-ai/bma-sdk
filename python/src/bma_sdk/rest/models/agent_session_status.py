from typing import Literal, cast

AgentSessionStatus = Literal["idle", "rescheduling", "running", "terminated"]

AGENT_SESSION_STATUS_VALUES: set[AgentSessionStatus] = {
    "idle",
    "rescheduling",
    "running",
    "terminated",
}


def check_agent_session_status(value: str) -> AgentSessionStatus:
    if value in AGENT_SESSION_STATUS_VALUES:
        return cast(AgentSessionStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_STATUS_VALUES!r}"
    )
