from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_subagent_type import (
    AgentConfigDefinitionSubagentType,
    check_agent_config_definition_subagent_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_subagent_instruction import (
        AgentConfigDefinitionSubagentInstruction,
    )
    from ..models.agent_config_definition_subagent_model import (
        AgentConfigDefinitionSubagentModel,
    )


T = TypeVar("T", bound="AgentConfigDefinitionSubagent")


@_attrs_define
class AgentConfigDefinitionSubagent:
    """
    Attributes:
        type_ (AgentConfigDefinitionSubagentType):
        archive_after_idle_minutes (Union[Unset, int]):
        description (Union[Unset, str]):
        instruction (Union[Unset, AgentConfigDefinitionSubagentInstruction]):
        max_instances (Union[Unset, int]):
        model (Union[Unset, AgentConfigDefinitionSubagentModel]):
        profile (Union[Unset, str]): Name of an existing resource, resolved when the config is compiled.
    """

    type_: AgentConfigDefinitionSubagentType
    archive_after_idle_minutes: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    instruction: Union[Unset, "AgentConfigDefinitionSubagentInstruction"] = UNSET
    max_instances: Union[Unset, int] = UNSET
    model: Union[Unset, "AgentConfigDefinitionSubagentModel"] = UNSET
    profile: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        archive_after_idle_minutes = self.archive_after_idle_minutes

        description = self.description

        instruction: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.instruction, Unset):
            instruction = self.instruction.to_dict()

        max_instances = self.max_instances

        model: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        profile = self.profile

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )
        if archive_after_idle_minutes is not UNSET:
            field_dict["archive_after_idle_minutes"] = archive_after_idle_minutes
        if description is not UNSET:
            field_dict["description"] = description
        if instruction is not UNSET:
            field_dict["instruction"] = instruction
        if max_instances is not UNSET:
            field_dict["max_instances"] = max_instances
        if model is not UNSET:
            field_dict["model"] = model
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_subagent_instruction import (
            AgentConfigDefinitionSubagentInstruction,
        )
        from ..models.agent_config_definition_subagent_model import (
            AgentConfigDefinitionSubagentModel,
        )

        d = dict(src_dict)
        type_ = check_agent_config_definition_subagent_type(d.pop("type"))

        archive_after_idle_minutes = d.pop("archive_after_idle_minutes", UNSET)

        description = d.pop("description", UNSET)

        _instruction = d.pop("instruction", UNSET)
        instruction: Union[Unset, AgentConfigDefinitionSubagentInstruction]
        if isinstance(_instruction, Unset):
            instruction = UNSET
        else:
            instruction = AgentConfigDefinitionSubagentInstruction.from_dict(
                _instruction
            )

        max_instances = d.pop("max_instances", UNSET)

        _model = d.pop("model", UNSET)
        model: Union[Unset, AgentConfigDefinitionSubagentModel]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = AgentConfigDefinitionSubagentModel.from_dict(_model)

        profile = d.pop("profile", UNSET)

        agent_config_definition_subagent = cls(
            type_=type_,
            archive_after_idle_minutes=archive_after_idle_minutes,
            description=description,
            instruction=instruction,
            max_instances=max_instances,
            model=model,
            profile=profile,
        )

        return agent_config_definition_subagent
