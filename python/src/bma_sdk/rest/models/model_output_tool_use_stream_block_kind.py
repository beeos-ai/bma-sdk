from typing import Literal, cast

ModelOutputToolUseStreamBlockKind = Literal["tool_use"]

MODEL_OUTPUT_TOOL_USE_STREAM_BLOCK_KIND_VALUES: set[
    ModelOutputToolUseStreamBlockKind
] = {
    "tool_use",
}


def check_model_output_tool_use_stream_block_kind(
    value: str,
) -> ModelOutputToolUseStreamBlockKind:
    if value in MODEL_OUTPUT_TOOL_USE_STREAM_BLOCK_KIND_VALUES:
        return cast(ModelOutputToolUseStreamBlockKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_TOOL_USE_STREAM_BLOCK_KIND_VALUES!r}"
    )
