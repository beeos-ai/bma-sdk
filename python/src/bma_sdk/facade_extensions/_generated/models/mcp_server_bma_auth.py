from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.mcp_server_bma_auth_type import (
    MCPServerBMAAuthType,
    check_mcp_server_bma_auth_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPServerBMAAuth")


@_attrs_define
class MCPServerBMAAuth:
    """`mcp_servers[].bma_auth` binds an MCP server to a BMA project secret.
    `service` and `region` are required for, and only allowed with,
    `type: sigv4`.

        Attributes:
            type_ (MCPServerBMAAuthType):
            secret_id (str):
            service (Union[Unset, str]):
            region (Union[Unset, str]):
    """

    type_: MCPServerBMAAuthType
    secret_id: str
    service: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        secret_id = self.secret_id

        service = self.service

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "secret_id": secret_id,
            }
        )
        if service is not UNSET:
            field_dict["service"] = service
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_mcp_server_bma_auth_type(d.pop("type"))

        secret_id = d.pop("secret_id")

        service = d.pop("service", UNSET)

        region = d.pop("region", UNSET)

        mcp_server_bma_auth = cls(
            type_=type_,
            secret_id=secret_id,
            service=service,
            region=region,
        )

        mcp_server_bma_auth.additional_properties = d
        return mcp_server_bma_auth

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
