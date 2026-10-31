from typing import Literal, cast

AgentMachineBindingKind = Literal["explicit", "pool"]

AGENT_MACHINE_BINDING_KIND_VALUES: set[AgentMachineBindingKind] = {
    "explicit",
    "pool",
}


def check_agent_machine_binding_kind(value: str) -> AgentMachineBindingKind:
    if value in AGENT_MACHINE_BINDING_KIND_VALUES:
        return cast(AgentMachineBindingKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MACHINE_BINDING_KIND_VALUES!r}"
    )
