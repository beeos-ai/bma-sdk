from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.desktop_action import DesktopAction


T = TypeVar("T", bound="DesktopAgentActionRequest")


@_attrs_define
class DesktopAgentActionRequest:
    """
    Attributes:
        generation (int):
        action (DesktopAction):
    """

    generation: int
    action: "DesktopAction"

    def to_dict(self) -> dict[str, Any]:
        generation = self.generation

        action = self.action.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "generation": generation,
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.desktop_action import DesktopAction

        d = dict(src_dict)
        generation = d.pop("generation")

        action = DesktopAction.from_dict(d.pop("action"))

        desktop_agent_action_request = cls(
            generation=generation,
            action=action,
        )

        return desktop_agent_action_request
