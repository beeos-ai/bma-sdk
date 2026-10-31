from typing import Literal, cast

AgentMachineKind = Literal["ephemeral", "persistent"]

AGENT_MACHINE_KIND_VALUES: set[AgentMachineKind] = {
    "ephemeral",
    "persistent",
}


def check_agent_machine_kind(value: str) -> AgentMachineKind:
    if value in AGENT_MACHINE_KIND_VALUES:
        return cast(AgentMachineKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MACHINE_KIND_VALUES!r}"
    )
