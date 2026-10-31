from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CompiledModelReasoning")


@_attrs_define
class CompiledModelReasoning:
    """
    Attributes:
        effort (str):
    """

    effort: str

    def to_dict(self) -> dict[str, Any]:
        effort = self.effort

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "effort": effort,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        effort = d.pop("effort")

        compiled_model_reasoning = cls(
            effort=effort,
        )

        return compiled_model_reasoning
