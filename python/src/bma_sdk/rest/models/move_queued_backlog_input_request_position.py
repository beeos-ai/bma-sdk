from typing import Literal, cast

MoveQueuedBacklogInputRequestPosition = Literal["after", "back", "before", "front"]

MOVE_QUEUED_BACKLOG_INPUT_REQUEST_POSITION_VALUES: set[
    MoveQueuedBacklogInputRequestPosition
] = {
    "after",
    "back",
    "before",
    "front",
}


def check_move_queued_backlog_input_request_position(
    value: str,
) -> MoveQueuedBacklogInputRequestPosition:
    if value in MOVE_QUEUED_BACKLOG_INPUT_REQUEST_POSITION_VALUES:
        return cast(MoveQueuedBacklogInputRequestPosition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MOVE_QUEUED_BACKLOG_INPUT_REQUEST_POSITION_VALUES!r}"
    )
