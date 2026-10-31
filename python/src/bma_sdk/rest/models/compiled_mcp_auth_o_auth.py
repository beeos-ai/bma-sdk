from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.compiled_mcp_auth_o_auth_type import (
    CompiledMCPAuthOAuthType,
    check_compiled_mcp_auth_o_auth_type,
)

T = TypeVar("T", bound="CompiledMCPAuthOAuth")


@_attrs_define
class CompiledMCPAuthOAuth:
    """
    Attributes:
        type_ (CompiledMCPAuthOAuthType):
        secret_id (str): Secret ID (sec_...).
    """

    type_: CompiledMCPAuthOAuthType
    secret_id: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        secret_id = self.secret_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "secret_id": secret_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_compiled_mcp_auth_o_auth_type(d.pop("type"))

        secret_id = d.pop("secret_id")

        compiled_mcp_auth_o_auth = cls(
            type_=type_,
            secret_id=secret_id,
        )

        return compiled_mcp_auth_o_auth
