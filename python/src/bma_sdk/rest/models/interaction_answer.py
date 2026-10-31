from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InteractionAnswer")


@_attrs_define
class InteractionAnswer:
    """
    Attributes:
        option_indices (list[int]):
        text (Union[Unset, str]): Optional companion text when the selected option allows it.
    """

    option_indices: list[int]
    text: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        option_indices = self.option_indices

        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "option_indices": option_indices,
            }
        )
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        option_indices = cast(list[int], d.pop("option_indices"))

        text = d.pop("text", UNSET)

        interaction_answer = cls(
            option_indices=option_indices,
            text=text,
        )

        return interaction_answer
