from typing import Literal, cast

AgentInteractionKind = Literal["permission", "question"]

AGENT_INTERACTION_KIND_VALUES: set[AgentInteractionKind] = {
    "permission",
    "question",
}


def check_agent_interaction_kind(value: str) -> AgentInteractionKind:
    if value in AGENT_INTERACTION_KIND_VALUES:
        return cast(AgentInteractionKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_INTERACTION_KIND_VALUES!r}"
    )
