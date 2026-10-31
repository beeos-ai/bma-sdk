from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigDefinitionSubagentInstruction")


@_attrs_define
class AgentConfigDefinitionSubagentInstruction:
    """
    Attributes:
        append (Union[Unset, str]):
    """

    append: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        append = self.append

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if append is not UNSET:
            field_dict["append"] = append

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        append = d.pop("append", UNSET)

        agent_config_definition_subagent_instruction = cls(
            append=append,
        )

        return agent_config_definition_subagent_instruction
