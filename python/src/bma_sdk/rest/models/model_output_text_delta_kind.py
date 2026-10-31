from typing import Literal, cast

ModelOutputTextDeltaKind = Literal["text_delta"]

MODEL_OUTPUT_TEXT_DELTA_KIND_VALUES: set[ModelOutputTextDeltaKind] = {
    "text_delta",
}


def check_model_output_text_delta_kind(value: str) -> ModelOutputTextDeltaKind:
    if value in MODEL_OUTPUT_TEXT_DELTA_KIND_VALUES:
        return cast(ModelOutputTextDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_TEXT_DELTA_KIND_VALUES!r}"
    )
