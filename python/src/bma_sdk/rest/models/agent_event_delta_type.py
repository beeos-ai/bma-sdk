from typing import Literal, cast

AgentEventDeltaType = Literal["agent_event_delta"]

AGENT_EVENT_DELTA_TYPE_VALUES: set[AgentEventDeltaType] = {
    "agent_event_delta",
}


def check_agent_event_delta_type(value: str) -> AgentEventDeltaType:
    if value in AGENT_EVENT_DELTA_TYPE_VALUES:
        return cast(AgentEventDeltaType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_EVENT_DELTA_TYPE_VALUES!r}"
    )
