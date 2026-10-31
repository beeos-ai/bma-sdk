from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_message_stop_delta_kind import (
    ModelOutputMessageStopDeltaKind,
    check_model_output_message_stop_delta_kind,
)

if TYPE_CHECKING:
    from ..models.model_output_message_stop_delta_stop import (
        ModelOutputMessageStopDeltaStop,
    )


T = TypeVar("T", bound="ModelOutputMessageStopDelta")


@_attrs_define
class ModelOutputMessageStopDelta:
    """
    Attributes:
        kind (ModelOutputMessageStopDeltaKind):
        stop (ModelOutputMessageStopDeltaStop):
    """

    kind: ModelOutputMessageStopDeltaKind
    stop: "ModelOutputMessageStopDeltaStop"

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        stop = self.stop.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "stop": stop,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_output_message_stop_delta_stop import (
            ModelOutputMessageStopDeltaStop,
        )

        d = dict(src_dict)
        kind = check_model_output_message_stop_delta_kind(d.pop("kind"))

        stop = ModelOutputMessageStopDeltaStop.from_dict(d.pop("stop"))

        model_output_message_stop_delta = cls(
            kind=kind,
            stop=stop,
        )

        return model_output_message_stop_delta
