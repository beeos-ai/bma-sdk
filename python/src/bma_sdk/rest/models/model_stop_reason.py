from typing import Literal, cast

ModelStopReason = Literal[
    "content_filter",
    "context_window",
    "end_turn",
    "max_tokens",
    "pause",
    "refusal",
    "tool_use",
    "unknown",
]

MODEL_STOP_REASON_VALUES: set[ModelStopReason] = {
    "content_filter",
    "context_window",
    "end_turn",
    "max_tokens",
    "pause",
    "refusal",
    "tool_use",
    "unknown",
}


def check_model_stop_reason(value: str) -> ModelStopReason:
    if value in MODEL_STOP_REASON_VALUES:
        return cast(ModelStopReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_STOP_REASON_VALUES!r}"
    )
