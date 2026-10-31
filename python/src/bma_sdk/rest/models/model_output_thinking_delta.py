from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_thinking_delta_kind import (
    ModelOutputThinkingDeltaKind,
    check_model_output_thinking_delta_kind,
)

T = TypeVar("T", bound="ModelOutputThinkingDelta")


@_attrs_define
class ModelOutputThinkingDelta:
    """
    Attributes:
        kind (ModelOutputThinkingDeltaKind):
        block_index (int):
        delta (str):
    """

    kind: ModelOutputThinkingDeltaKind
    block_index: int
    delta: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        block_index = self.block_index

        delta = self.delta

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "block_index": block_index,
                "delta": delta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_model_output_thinking_delta_kind(d.pop("kind"))

        block_index = d.pop("block_index")

        delta = d.pop("delta")

        model_output_thinking_delta = cls(
            kind=kind,
            block_index=block_index,
            delta=delta,
        )

        return model_output_thinking_delta
