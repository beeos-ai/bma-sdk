from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.compiled_mcp_auth_sig_v4_type import (
    CompiledMCPAuthSigV4Type,
    check_compiled_mcp_auth_sig_v4_type,
)

T = TypeVar("T", bound="CompiledMCPAuthSigV4")


@_attrs_define
class CompiledMCPAuthSigV4:
    """
    Attributes:
        type_ (CompiledMCPAuthSigV4Type):
        secret_id (str): Secret ID (sec_...).
        service (str):
        region (str):
    """

    type_: CompiledMCPAuthSigV4Type
    secret_id: str
    service: str
    region: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        secret_id = self.secret_id

        service = self.service

        region = self.region

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "secret_id": secret_id,
                "service": service,
                "region": region,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_compiled_mcp_auth_sig_v4_type(d.pop("type"))

        secret_id = d.pop("secret_id")

        service = d.pop("service")

        region = d.pop("region")

        compiled_mcp_auth_sig_v4 = cls(
            type_=type_,
            secret_id=secret_id,
            service=service,
            region=region,
        )

        return compiled_mcp_auth_sig_v4
