from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.mcp_server_auth_required_error_code import (
    MCPServerAuthRequiredErrorCode,
    check_mcp_server_auth_required_error_code,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_server_auth_hint import MCPServerAuthHint


T = TypeVar("T", bound="MCPServerAuthRequiredError")


@_attrs_define
class MCPServerAuthRequiredError:
    """
    Attributes:
        error (str): Human-readable error message. Do not match on it programmatically.
        code (MCPServerAuthRequiredErrorCode):
        auth (Union[Unset, MCPServerAuthHint]):
    """

    error: str
    code: MCPServerAuthRequiredErrorCode
    auth: Union[Unset, "MCPServerAuthHint"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code: str = self.code

        auth: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "code": code,
            }
        )
        if auth is not UNSET:
            field_dict["auth"] = auth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_server_auth_hint import MCPServerAuthHint

        d = dict(src_dict)
        error = d.pop("error")

        code = check_mcp_server_auth_required_error_code(d.pop("code"))

        _auth = d.pop("auth", UNSET)
        auth: Union[Unset, MCPServerAuthHint]
        if isinstance(_auth, Unset):
            auth = UNSET
        else:
            auth = MCPServerAuthHint.from_dict(_auth)

        mcp_server_auth_required_error = cls(
            error=error,
            code=code,
            auth=auth,
        )

        return mcp_server_auth_required_error
