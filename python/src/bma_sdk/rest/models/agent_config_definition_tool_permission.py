from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_tool_permission_parameters import (
        AgentConfigDefinitionToolPermissionParameters,
    )


T = TypeVar("T", bound="AgentConfigDefinitionToolPermission")


@_attrs_define
class AgentConfigDefinitionToolPermission:
    """
    Attributes:
        mode (str):
        parameters (Union[Unset, AgentConfigDefinitionToolPermissionParameters]):
    """

    mode: str
    parameters: Union[Unset, "AgentConfigDefinitionToolPermissionParameters"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
            }
        )
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_tool_permission_parameters import (
            AgentConfigDefinitionToolPermissionParameters,
        )

        d = dict(src_dict)
        mode = d.pop("mode")

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, AgentConfigDefinitionToolPermissionParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = AgentConfigDefinitionToolPermissionParameters.from_dict(
                _parameters
            )

        agent_config_definition_tool_permission = cls(
            mode=mode,
            parameters=parameters,
        )

        return agent_config_definition_tool_permission
