from typing import Literal, cast

ModelProviderAPIVariant = Literal["bedrock", "default", "openrouter"]

MODEL_PROVIDER_API_VARIANT_VALUES: set[ModelProviderAPIVariant] = {
    "bedrock",
    "default",
    "openrouter",
}


def check_model_provider_api_variant(value: str) -> ModelProviderAPIVariant:
    if value in MODEL_PROVIDER_API_VARIANT_VALUES:
        return cast(ModelProviderAPIVariant, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_PROVIDER_API_VARIANT_VALUES!r}"
    )
