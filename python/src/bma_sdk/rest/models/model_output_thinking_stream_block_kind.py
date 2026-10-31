from typing import Literal, cast

ModelOutputThinkingStreamBlockKind = Literal["thinking"]

MODEL_OUTPUT_THINKING_STREAM_BLOCK_KIND_VALUES: set[
    ModelOutputThinkingStreamBlockKind
] = {
    "thinking",
}


def check_model_output_thinking_stream_block_kind(
    value: str,
) -> ModelOutputThinkingStreamBlockKind:
    if value in MODEL_OUTPUT_THINKING_STREAM_BLOCK_KIND_VALUES:
        return cast(ModelOutputThinkingStreamBlockKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_THINKING_STREAM_BLOCK_KIND_VALUES!r}"
    )
