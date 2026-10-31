from typing import Literal, cast

ModelOutputErrorDeltaKind = Literal["error"]

MODEL_OUTPUT_ERROR_DELTA_KIND_VALUES: set[ModelOutputErrorDeltaKind] = {
    "error",
}


def check_model_output_error_delta_kind(value: str) -> ModelOutputErrorDeltaKind:
    if value in MODEL_OUTPUT_ERROR_DELTA_KIND_VALUES:
        return cast(ModelOutputErrorDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_ERROR_DELTA_KIND_VALUES!r}"
    )
