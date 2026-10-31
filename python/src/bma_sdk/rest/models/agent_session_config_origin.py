from typing import Literal, cast

AgentSessionConfigOrigin = Literal["agent", "session"]

AGENT_SESSION_CONFIG_ORIGIN_VALUES: set[AgentSessionConfigOrigin] = {
    "agent",
    "session",
}


def check_agent_session_config_origin(value: str) -> AgentSessionConfigOrigin:
    if value in AGENT_SESSION_CONFIG_ORIGIN_VALUES:
        return cast(AgentSessionConfigOrigin, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_SESSION_CONFIG_ORIGIN_VALUES!r}"
    )
