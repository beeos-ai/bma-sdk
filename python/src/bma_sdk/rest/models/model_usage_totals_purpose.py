from typing import Literal, cast

ModelUsageTotalsPurpose = Literal["harness", "title", "turn"]

MODEL_USAGE_TOTALS_PURPOSE_VALUES: set[ModelUsageTotalsPurpose] = {
    "harness",
    "title",
    "turn",
}


def check_model_usage_totals_purpose(value: str) -> ModelUsageTotalsPurpose:
    if value in MODEL_USAGE_TOTALS_PURPOSE_VALUES:
        return cast(ModelUsageTotalsPurpose, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_USAGE_TOTALS_PURPOSE_VALUES!r}"
    )
