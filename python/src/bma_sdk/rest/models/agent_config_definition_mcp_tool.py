from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_tool_permission import (
        AgentConfigDefinitionToolPermission,
    )


T = TypeVar("T", bound="AgentConfigDefinitionMCPTool")


@_attrs_define
class AgentConfigDefinitionMCPTool:
    """
    Attributes:
        deferred (Union[None, Unset, bool]):
        enabled (Union[None, Unset, bool]):
        permission (Union[Unset, AgentConfigDefinitionToolPermission]):
    """

    deferred: Union[None, Unset, bool] = UNSET
    enabled: Union[None, Unset, bool] = UNSET
    permission: Union[Unset, "AgentConfigDefinitionToolPermission"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        deferred: Union[None, Unset, bool]
        if isinstance(self.deferred, Unset):
            deferred = UNSET
        else:
            deferred = self.deferred

        enabled: Union[None, Unset, bool]
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        permission: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_tool_permission import (
            AgentConfigDefinitionToolPermission,
        )

        d = dict(src_dict)

        def _parse_deferred(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        deferred = _parse_deferred(d.pop("deferred", UNSET))

        def _parse_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, AgentConfigDefinitionToolPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = AgentConfigDefinitionToolPermission.from_dict(_permission)

        agent_config_definition_mcp_tool = cls(
            deferred=deferred,
            enabled=enabled,
            permission=permission,
        )

        return agent_config_definition_mcp_tool
