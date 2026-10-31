from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.mcp_server_auth_none_type import (
    MCPServerAuthNoneType,
    check_mcp_server_auth_none_type,
)

T = TypeVar("T", bound="MCPServerAuthNone")


@_attrs_define
class MCPServerAuthNone:
    """
    Attributes:
        type_ (MCPServerAuthNoneType):
    """

    type_: MCPServerAuthNoneType

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_mcp_server_auth_none_type(d.pop("type"))

        mcp_server_auth_none = cls(
            type_=type_,
        )

        return mcp_server_auth_none
