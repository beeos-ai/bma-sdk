from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DesktopGenerationRequest")


@_attrs_define
class DesktopGenerationRequest:
    """
    Attributes:
        generation (int):
    """

    generation: int

    def to_dict(self) -> dict[str, Any]:
        generation = self.generation

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "generation": generation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        generation = d.pop("generation")

        desktop_generation_request = cls(
            generation=generation,
        )

        return desktop_generation_request
