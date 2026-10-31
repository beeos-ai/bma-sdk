from typing import Literal, cast

CreateModelProviderConfigRequestPreset = Literal["anthropic", "openai", "openrouter"]

CREATE_MODEL_PROVIDER_CONFIG_REQUEST_PRESET_VALUES: set[
    CreateModelProviderConfigRequestPreset
] = {
    "anthropic",
    "openai",
    "openrouter",
}


def check_create_model_provider_config_request_preset(
    value: str,
) -> CreateModelProviderConfigRequestPreset:
    if value in CREATE_MODEL_PROVIDER_CONFIG_REQUEST_PRESET_VALUES:
        return cast(CreateModelProviderConfigRequestPreset, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_MODEL_PROVIDER_CONFIG_REQUEST_PRESET_VALUES!r}"
    )
