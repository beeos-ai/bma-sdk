from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

T = TypeVar("T", bound="ChatIntegrationLauncher")


@_attrs_define
class ChatIntegrationLauncher:
    """
    Attributes:
        profiles (list[str]): One profile launches immediately; several offer a choice of exactly one.
    """

    profiles: list[str]

    def to_dict(self) -> dict[str, Any]:
        profiles = self.profiles

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "profiles": profiles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profiles = cast(list[str], d.pop("profiles"))

        chat_integration_launcher = cls(
            profiles=profiles,
        )

        return chat_integration_launcher
