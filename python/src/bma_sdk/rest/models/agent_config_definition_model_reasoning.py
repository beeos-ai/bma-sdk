from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentConfigDefinitionModelReasoning")


@_attrs_define
class AgentConfigDefinitionModelReasoning:
    """
    Attributes:
        effort (str):
    """

    effort: str

    def to_dict(self) -> dict[str, Any]:
        effort = self.effort

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "effort": effort,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        effort = d.pop("effort")

        agent_config_definition_model_reasoning = cls(
            effort=effort,
        )

        return agent_config_definition_model_reasoning
