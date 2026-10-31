from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentConfigGeneratedSource")


@_attrs_define
class AgentConfigGeneratedSource:
    """
    Attributes:
        source (str):
    """

    source: str

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        agent_config_generated_source = cls(
            source=source,
        )

        return agent_config_generated_source
