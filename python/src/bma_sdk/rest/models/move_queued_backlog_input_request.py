from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.move_queued_backlog_input_request_position import (
    MoveQueuedBacklogInputRequestPosition,
    check_move_queued_backlog_input_request_position,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MoveQueuedBacklogInputRequest")


@_attrs_define
class MoveQueuedBacklogInputRequest:
    """
    Attributes:
        position (MoveQueuedBacklogInputRequestPosition):
        anchor_input_id (Union[Unset, str]):
    """

    position: MoveQueuedBacklogInputRequestPosition
    anchor_input_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        position: str = self.position

        anchor_input_id = self.anchor_input_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "position": position,
            }
        )
        if anchor_input_id is not UNSET:
            field_dict["anchor_input_id"] = anchor_input_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        position = check_move_queued_backlog_input_request_position(d.pop("position"))

        anchor_input_id = d.pop("anchor_input_id", UNSET)

        move_queued_backlog_input_request = cls(
            position=position,
            anchor_input_id=anchor_input_id,
        )

        return move_queued_backlog_input_request
