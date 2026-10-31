from typing import Literal, cast

ModelProviderAuthKind = Literal["api_key_header", "bearer_token", "sigv4"]

MODEL_PROVIDER_AUTH_KIND_VALUES: set[ModelProviderAuthKind] = {
    "api_key_header",
    "bearer_token",
    "sigv4",
}


def check_model_provider_auth_kind(value: str) -> ModelProviderAuthKind:
    if value in MODEL_PROVIDER_AUTH_KIND_VALUES:
        return cast(ModelProviderAuthKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_PROVIDER_AUTH_KIND_VALUES!r}"
    )
