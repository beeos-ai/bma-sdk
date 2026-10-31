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
    from ..models.desktop_capabilities_request import DesktopCapabilitiesRequest


T = TypeVar("T", bound="CreateDesktopSessionRequest")


@_attrs_define
class CreateDesktopSessionRequest:
    """
    Attributes:
        agent_id (Union[Unset, str]):
        read_only (Union[Unset, bool]):  Default: False.
        lease_seconds (Union[Unset, int]):
        capabilities (Union[Unset, DesktopCapabilitiesRequest]):
    """

    agent_id: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = False
    lease_seconds: Union[Unset, int] = UNSET
    capabilities: Union[Unset, "DesktopCapabilitiesRequest"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        read_only = self.read_only

        lease_seconds = self.lease_seconds

        capabilities: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if read_only is not UNSET:
            field_dict["read_only"] = read_only
        if lease_seconds is not UNSET:
            field_dict["lease_seconds"] = lease_seconds
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.desktop_capabilities_request import DesktopCapabilitiesRequest

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        read_only = d.pop("read_only", UNSET)

        lease_seconds = d.pop("lease_seconds", UNSET)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: Union[Unset, DesktopCapabilitiesRequest]
        if isinstance(_capabilities, Unset):
            capabilities = UNSET
        else:
            capabilities = DesktopCapabilitiesRequest.from_dict(_capabilities)

        create_desktop_session_request = cls(
            agent_id=agent_id,
            read_only=read_only,
            lease_seconds=lease_seconds,
            capabilities=capabilities,
        )

        return create_desktop_session_request
