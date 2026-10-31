from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromoteQueuedInputToSteeringRequest")


@_attrs_define
class PromoteQueuedInputToSteeringRequest:
    """
    Attributes:
        cancel_open_interactions (Union[Unset, bool]): When true, atomically cancels open interactions associated with
            the current turn's unfinished tool calls as this queued input becomes steering. Their parent tool calls complete
            as canceled; the turn, runtime, and unrelated tool calls are preserved.
    """

    cancel_open_interactions: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        cancel_open_interactions = self.cancel_open_interactions

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if cancel_open_interactions is not UNSET:
            field_dict["cancel_open_interactions"] = cancel_open_interactions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancel_open_interactions = d.pop("cancel_open_interactions", UNSET)

        promote_queued_input_to_steering_request = cls(
            cancel_open_interactions=cancel_open_interactions,
        )

        return promote_queued_input_to_steering_request
