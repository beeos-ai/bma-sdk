from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentConfigDefinitionInteractionHandler")


@_attrs_define
class AgentConfigDefinitionInteractionHandler:
    """Enables an integration's interaction handler. Takes no settings."""

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        agent_config_definition_interaction_handler = cls()

        return agent_config_definition_interaction_handler
