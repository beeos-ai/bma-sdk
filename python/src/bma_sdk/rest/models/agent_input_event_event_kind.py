from typing import Literal, cast

AgentInputEventEventKind = Literal["agent_input"]

AGENT_INPUT_EVENT_EVENT_KIND_VALUES: set[AgentInputEventEventKind] = {
    "agent_input",
}


def check_agent_input_event_event_kind(value: str) -> AgentInputEventEventKind:
    if value in AGENT_INPUT_EVENT_EVENT_KIND_VALUES:
        return cast(AgentInputEventEventKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_INPUT_EVENT_EVENT_KIND_VALUES!r}"
    )
