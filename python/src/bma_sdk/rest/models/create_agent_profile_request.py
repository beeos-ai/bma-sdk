from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateAgentProfileRequest")


@_attrs_define
class CreateAgentProfileRequest:
    """
    Attributes:
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        config (str): Agent config ID (acfg_...).
    """

    name: str
    config: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        config = self.config

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        config = d.pop("config")

        create_agent_profile_request = cls(
            name=name,
            config=config,
        )

        return create_agent_profile_request
