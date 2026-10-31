from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_text_stream_block_kind import (
    ModelOutputTextStreamBlockKind,
    check_model_output_text_stream_block_kind,
)

T = TypeVar("T", bound="ModelOutputTextStreamBlock")


@_attrs_define
class ModelOutputTextStreamBlock:
    """
    Attributes:
        kind (ModelOutputTextStreamBlockKind):
    """

    kind: ModelOutputTextStreamBlockKind

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_model_output_text_stream_block_kind(d.pop("kind"))

        model_output_text_stream_block = cls(
            kind=kind,
        )

        return model_output_text_stream_block
