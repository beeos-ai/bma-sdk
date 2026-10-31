from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="InteractionFormContextItem")


@_attrs_define
class InteractionFormContextItem:
    """
    Attributes:
        label (str):
        value (str):
    """

    label: str
    value: str

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "label": label,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        value = d.pop("value")

        interaction_form_context_item = cls(
            label=label,
            value=value,
        )

        return interaction_form_context_item
