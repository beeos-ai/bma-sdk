from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DesktopActionResponse")


@_attrs_define
class DesktopActionResponse:
    """
    Attributes:
        seq (int):
    """

    seq: int

    def to_dict(self) -> dict[str, Any]:
        seq = self.seq

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "seq": seq,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        seq = d.pop("seq")

        desktop_action_response = cls(
            seq=seq,
        )

        return desktop_action_response
