from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentModel")


@_attrs_define
class AgentModel:
    """
    Attributes:
        provider_config (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace
            and invisible or control characters are not.
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
    """

    provider_config: str
    name: str

    def to_dict(self) -> dict[str, Any]:
        provider_config = self.provider_config

        name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_config": provider_config,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_config = d.pop("provider_config")

        name = d.pop("name")

        agent_model = cls(
            provider_config=provider_config,
            name=name,
        )

        return agent_model
