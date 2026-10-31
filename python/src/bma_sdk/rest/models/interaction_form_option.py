from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InteractionFormOption")


@_attrs_define
class InteractionFormOption:
    """
    Attributes:
        label (str):
        allows_text (Union[Unset, bool]): Whether the answer may include optional companion text for this option.
            Default: False.
    """

    label: str
    allows_text: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        allows_text = self.allows_text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "label": label,
            }
        )
        if allows_text is not UNSET:
            field_dict["allows_text"] = allows_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        allows_text = d.pop("allows_text", UNSET)

        interaction_form_option = cls(
            label=label,
            allows_text=allows_text,
        )

        return interaction_form_option
