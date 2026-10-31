from typing import Literal, cast

ModelOutputThinkingDeltaKind = Literal["thinking_delta"]

MODEL_OUTPUT_THINKING_DELTA_KIND_VALUES: set[ModelOutputThinkingDeltaKind] = {
    "thinking_delta",
}


def check_model_output_thinking_delta_kind(value: str) -> ModelOutputThinkingDeltaKind:
    if value in MODEL_OUTPUT_THINKING_DELTA_KIND_VALUES:
        return cast(ModelOutputThinkingDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_THINKING_DELTA_KIND_VALUES!r}"
    )
