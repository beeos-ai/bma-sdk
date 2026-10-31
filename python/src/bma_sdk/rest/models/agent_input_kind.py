from typing import Literal, cast

AgentInputKind = Literal["config_change", "content", "control", "interaction_response"]

AGENT_INPUT_KIND_VALUES: set[AgentInputKind] = {
    "config_change",
    "content",
    "control",
    "interaction_response",
}


def check_agent_input_kind(value: str) -> AgentInputKind:
    if value in AGENT_INPUT_KIND_VALUES:
        return cast(AgentInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_INPUT_KIND_VALUES!r}"
    )
