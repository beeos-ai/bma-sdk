from typing import Literal, cast

AgentModelOverrideProviderApiFormat = Literal[
    "anthropic-messages", "openai-chat-completions", "openai-responses"
]

AGENT_MODEL_OVERRIDE_PROVIDER_API_FORMAT_VALUES: set[
    AgentModelOverrideProviderApiFormat
] = {
    "anthropic-messages",
    "openai-chat-completions",
    "openai-responses",
}


def check_agent_model_override_provider_api_format(
    value: str,
) -> AgentModelOverrideProviderApiFormat:
    if value in AGENT_MODEL_OVERRIDE_PROVIDER_API_FORMAT_VALUES:
        return cast(AgentModelOverrideProviderApiFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MODEL_OVERRIDE_PROVIDER_API_FORMAT_VALUES!r}"
    )
