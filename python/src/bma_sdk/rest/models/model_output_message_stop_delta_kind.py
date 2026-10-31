from typing import Literal, cast

ModelOutputMessageStopDeltaKind = Literal["message_stop"]

MODEL_OUTPUT_MESSAGE_STOP_DELTA_KIND_VALUES: set[ModelOutputMessageStopDeltaKind] = {
    "message_stop",
}


def check_model_output_message_stop_delta_kind(
    value: str,
) -> ModelOutputMessageStopDeltaKind:
    if value in MODEL_OUTPUT_MESSAGE_STOP_DELTA_KIND_VALUES:
        return cast(ModelOutputMessageStopDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_MESSAGE_STOP_DELTA_KIND_VALUES!r}"
    )
