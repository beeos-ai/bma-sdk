from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.desktop_action import DesktopAction


T = TypeVar("T", bound="DesktopActionRequest")


@_attrs_define
class DesktopActionRequest:
    """
    Attributes:
        seq (int):
        action (DesktopAction):
    """

    seq: int
    action: "DesktopAction"

    def to_dict(self) -> dict[str, Any]:
        seq = self.seq

        action = self.action.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "seq": seq,
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.desktop_action import DesktopAction

        d = dict(src_dict)
        seq = d.pop("seq")

        action = DesktopAction.from_dict(d.pop("action"))

        desktop_action_request = cls(
            seq=seq,
            action=action,
        )

        return desktop_action_request
