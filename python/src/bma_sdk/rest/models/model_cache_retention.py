from typing import Literal, cast

ModelCacheRetention = Literal["long", "none", "short"]

MODEL_CACHE_RETENTION_VALUES: set[ModelCacheRetention] = {
    "long",
    "none",
    "short",
}


def check_model_cache_retention(value: str) -> ModelCacheRetention:
    if value in MODEL_CACHE_RETENTION_VALUES:
        return cast(ModelCacheRetention, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_CACHE_RETENTION_VALUES!r}"
    )
