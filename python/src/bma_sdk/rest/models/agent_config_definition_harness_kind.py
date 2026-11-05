from typing import Literal, cast

AgentConfigDefinitionHarnessKind = Literal["acp", "bma"]

AGENT_CONFIG_DEFINITION_HARNESS_KIND_VALUES: set[AgentConfigDefinitionHarnessKind] = {
    "acp",
    "bma",
}


def check_agent_config_definition_harness_kind(
    value: str,
) -> AgentConfigDefinitionHarnessKind:
    if value in AGENT_CONFIG_DEFINITION_HARNESS_KIND_VALUES:
        return cast(AgentConfigDefinitionHarnessKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_HARNESS_KIND_VALUES!r}"
    )
