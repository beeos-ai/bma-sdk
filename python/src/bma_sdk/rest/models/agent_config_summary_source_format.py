from typing import Literal, cast

AgentConfigSummarySourceFormat = Literal["json", "yaml"]

AGENT_CONFIG_SUMMARY_SOURCE_FORMAT_VALUES: set[AgentConfigSummarySourceFormat] = {
    "json",
    "yaml",
}


def check_agent_config_summary_source_format(
    value: str,
) -> AgentConfigSummarySourceFormat:
    if value in AGENT_CONFIG_SUMMARY_SOURCE_FORMAT_VALUES:
        return cast(AgentConfigSummarySourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_SUMMARY_SOURCE_FORMAT_VALUES!r}"
    )
