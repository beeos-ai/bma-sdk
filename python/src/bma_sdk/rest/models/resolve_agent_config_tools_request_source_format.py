from typing import Literal, cast

ResolveAgentConfigToolsRequestSourceFormat = Literal["json", "yaml"]

RESOLVE_AGENT_CONFIG_TOOLS_REQUEST_SOURCE_FORMAT_VALUES: set[
    ResolveAgentConfigToolsRequestSourceFormat
] = {
    "json",
    "yaml",
}


def check_resolve_agent_config_tools_request_source_format(
    value: str,
) -> ResolveAgentConfigToolsRequestSourceFormat:
    if value in RESOLVE_AGENT_CONFIG_TOOLS_REQUEST_SOURCE_FORMAT_VALUES:
        return cast(ResolveAgentConfigToolsRequestSourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {RESOLVE_AGENT_CONFIG_TOOLS_REQUEST_SOURCE_FORMAT_VALUES!r}"
    )
