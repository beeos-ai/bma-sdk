from typing import Literal, cast

AgentMachineBindingState = Literal["attached", "released"]

AGENT_MACHINE_BINDING_STATE_VALUES: set[AgentMachineBindingState] = {
    "attached",
    "released",
}


def check_agent_machine_binding_state(value: str) -> AgentMachineBindingState:
    if value in AGENT_MACHINE_BINDING_STATE_VALUES:
        return cast(AgentMachineBindingState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MACHINE_BINDING_STATE_VALUES!r}"
    )
