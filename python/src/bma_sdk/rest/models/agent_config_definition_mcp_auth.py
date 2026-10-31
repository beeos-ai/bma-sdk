from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_mcp_auth_type import (
    AgentConfigDefinitionMCPAuthType,
    check_agent_config_definition_mcp_auth_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigDefinitionMCPAuth")


@_attrs_define
class AgentConfigDefinitionMCPAuth:
    """
    Attributes:
        secret_id (str):
        type_ (AgentConfigDefinitionMCPAuthType):
        region (Union[Unset, str]):
        service (Union[Unset, str]):
    """

    secret_id: str
    type_: AgentConfigDefinitionMCPAuthType
    region: Union[Unset, str] = UNSET
    service: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        secret_id = self.secret_id

        type_: str = self.type_

        region = self.region

        service = self.service

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "secret_id": secret_id,
                "type": type_,
            }
        )
        if region is not UNSET:
            field_dict["region"] = region
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        secret_id = d.pop("secret_id")

        type_ = check_agent_config_definition_mcp_auth_type(d.pop("type"))

        region = d.pop("region", UNSET)

        service = d.pop("service", UNSET)

        agent_config_definition_mcp_auth = cls(
            secret_id=secret_id,
            type_=type_,
            region=region,
            service=service,
        )

        return agent_config_definition_mcp_auth
