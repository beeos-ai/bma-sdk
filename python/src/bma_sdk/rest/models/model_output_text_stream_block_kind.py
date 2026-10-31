from typing import Literal, cast

ModelOutputTextStreamBlockKind = Literal["text"]

MODEL_OUTPUT_TEXT_STREAM_BLOCK_KIND_VALUES: set[ModelOutputTextStreamBlockKind] = {
    "text",
}


def check_model_output_text_stream_block_kind(
    value: str,
) -> ModelOutputTextStreamBlockKind:
    if value in MODEL_OUTPUT_TEXT_STREAM_BLOCK_KIND_VALUES:
        return cast(ModelOutputTextStreamBlockKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_TEXT_STREAM_BLOCK_KIND_VALUES!r}"
    )
