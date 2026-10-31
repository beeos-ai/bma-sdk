from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_stop_reason import ModelStopReason, check_model_stop_reason

if TYPE_CHECKING:
    from ..models.model_usage import ModelUsage


T = TypeVar("T", bound="ModelOutputMessageStopDeltaStop")


@_attrs_define
class ModelOutputMessageStopDeltaStop:
    """
    Attributes:
        reason (ModelStopReason):
        usage (ModelUsage): Token counts the provider reported for one model call. Cache and reasoning counts are
            omitted when the provider reported none.
    """

    reason: ModelStopReason
    usage: "ModelUsage"

    def to_dict(self) -> dict[str, Any]:
        reason: str = self.reason

        usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "reason": reason,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_usage import ModelUsage

        d = dict(src_dict)
        reason = check_model_stop_reason(d.pop("reason"))

        usage = ModelUsage.from_dict(d.pop("usage"))

        model_output_message_stop_delta_stop = cls(
            reason=reason,
            usage=usage,
        )

        return model_output_message_stop_delta_stop
