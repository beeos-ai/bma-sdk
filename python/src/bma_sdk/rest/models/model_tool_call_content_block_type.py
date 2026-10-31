from typing import Literal, cast

ModelToolCallContentBlockType = Literal["tool_call"]

MODEL_TOOL_CALL_CONTENT_BLOCK_TYPE_VALUES: set[ModelToolCallContentBlockType] = {
    "tool_call",
}


def check_model_tool_call_content_block_type(
    value: str,
) -> ModelToolCallContentBlockType:
    if value in MODEL_TOOL_CALL_CONTENT_BLOCK_TYPE_VALUES:
        return cast(ModelToolCallContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_TOOL_CALL_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
