from typing import Literal, cast

ModelOutputEventEventKind = Literal["model_output"]

MODEL_OUTPUT_EVENT_EVENT_KIND_VALUES: set[ModelOutputEventEventKind] = {
    "model_output",
}


def check_model_output_event_event_kind(value: str) -> ModelOutputEventEventKind:
    if value in MODEL_OUTPUT_EVENT_EVENT_KIND_VALUES:
        return cast(ModelOutputEventEventKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_EVENT_EVENT_KIND_VALUES!r}"
    )
