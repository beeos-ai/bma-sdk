from typing import Literal, cast

ContextCheckpointEventEventKind = Literal["context_checkpoint"]

CONTEXT_CHECKPOINT_EVENT_EVENT_KIND_VALUES: set[ContextCheckpointEventEventKind] = {
    "context_checkpoint",
}


def check_context_checkpoint_event_event_kind(
    value: str,
) -> ContextCheckpointEventEventKind:
    if value in CONTEXT_CHECKPOINT_EVENT_EVENT_KIND_VALUES:
        return cast(ContextCheckpointEventEventKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CONTEXT_CHECKPOINT_EVENT_EVENT_KIND_VALUES!r}"
    )
