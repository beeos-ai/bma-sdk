from typing import Literal, cast

AgentModelOverrideProviderApiVariant = Literal["default", "openrouter"]

AGENT_MODEL_OVERRIDE_PROVIDER_API_VARIANT_VALUES: set[
    AgentModelOverrideProviderApiVariant
] = {
    "default",
    "openrouter",
}


def check_agent_model_override_provider_api_variant(
    value: str,
) -> AgentModelOverrideProviderApiVariant:
    if value in AGENT_MODEL_OVERRIDE_PROVIDER_API_VARIANT_VALUES:
        return cast(AgentModelOverrideProviderApiVariant, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MODEL_OVERRIDE_PROVIDER_API_VARIANT_VALUES!r}"
    )
