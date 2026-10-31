from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.interaction_form_option import InteractionFormOption


T = TypeVar("T", bound="InteractionFormQuestion")


@_attrs_define
class InteractionFormQuestion:
    """
    Attributes:
        prompt (str):
        options (list['InteractionFormOption']):
        multiple (Union[Unset, bool]): Whether the answer may select more than one option. Default: False.
    """

    prompt: str
    options: list["InteractionFormOption"]
    multiple: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        multiple = self.multiple

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "prompt": prompt,
                "options": options,
            }
        )
        if multiple is not UNSET:
            field_dict["multiple"] = multiple

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interaction_form_option import InteractionFormOption

        d = dict(src_dict)
        prompt = d.pop("prompt")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = InteractionFormOption.from_dict(options_item_data)

            options.append(options_item)

        multiple = d.pop("multiple", UNSET)

        interaction_form_question = cls(
            prompt=prompt,
            options=options,
            multiple=multiple,
        )

        return interaction_form_question
