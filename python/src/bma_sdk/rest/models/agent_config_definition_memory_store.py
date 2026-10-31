from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_memory_store_access import (
    AgentConfigDefinitionMemoryStoreAccess,
    check_agent_config_definition_memory_store_access,
)

T = TypeVar("T", bound="AgentConfigDefinitionMemoryStore")


@_attrs_define
class AgentConfigDefinitionMemoryStore:
    """
    Attributes:
        name (str): Machine-readable memory store identifier consisting of lowercase ASCII segments separated by single
            hyphens.
        access (AgentConfigDefinitionMemoryStoreAccess):
    """

    name: str
    access: AgentConfigDefinitionMemoryStoreAccess

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        access: str = self.access

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "access": access,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        access = check_agent_config_definition_memory_store_access(d.pop("access"))

        agent_config_definition_memory_store = cls(
            name=name,
            access=access,
        )

        return agent_config_definition_memory_store
