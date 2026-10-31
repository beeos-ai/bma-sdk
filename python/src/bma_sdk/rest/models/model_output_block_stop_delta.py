from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_block_stop_delta_kind import (
    ModelOutputBlockStopDeltaKind,
    check_model_output_block_stop_delta_kind,
)

T = TypeVar("T", bound="ModelOutputBlockStopDelta")


@_attrs_define
class ModelOutputBlockStopDelta:
    """
    Attributes:
        kind (ModelOutputBlockStopDeltaKind):
        block_index (int):
    """

    kind: ModelOutputBlockStopDeltaKind
    block_index: int

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        block_index = self.block_index

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "block_index": block_index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_model_output_block_stop_delta_kind(d.pop("kind"))

        block_index = d.pop("block_index")

        model_output_block_stop_delta = cls(
            kind=kind,
            block_index=block_index,
        )

        return model_output_block_stop_delta
