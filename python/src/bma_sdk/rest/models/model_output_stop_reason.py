from typing import Literal, cast

ModelOutputStopReason = Literal[
    "content_filter", "end_turn", "error", "max_tokens", "refusal", "tool_use"
]

MODEL_OUTPUT_STOP_REASON_VALUES: set[ModelOutputStopReason] = {
    "content_filter",
    "end_turn",
    "error",
    "max_tokens",
    "refusal",
    "tool_use",
}


def check_model_output_stop_reason(value: str) -> ModelOutputStopReason:
    if value in MODEL_OUTPUT_STOP_REASON_VALUES:
        return cast(ModelOutputStopReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_STOP_REASON_VALUES!r}"
    )
