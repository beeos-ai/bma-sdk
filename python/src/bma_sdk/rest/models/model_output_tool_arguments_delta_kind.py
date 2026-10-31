from typing import Literal, cast

ModelOutputToolArgumentsDeltaKind = Literal["tool_arguments_delta"]

MODEL_OUTPUT_TOOL_ARGUMENTS_DELTA_KIND_VALUES: set[
    ModelOutputToolArgumentsDeltaKind
] = {
    "tool_arguments_delta",
}


def check_model_output_tool_arguments_delta_kind(
    value: str,
) -> ModelOutputToolArgumentsDeltaKind:
    if value in MODEL_OUTPUT_TOOL_ARGUMENTS_DELTA_KIND_VALUES:
        return cast(ModelOutputToolArgumentsDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_TOOL_ARGUMENTS_DELTA_KIND_VALUES!r}"
    )
