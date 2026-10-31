from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine_desktop_capability import MachineDesktopCapability
    from ..models.machine_interaction_permissions import MachineInteractionPermissions
    from ..models.machine_protocol_versions import MachineProtocolVersions
    from ..models.machine_terminal_capability import MachineTerminalCapability


T = TypeVar("T", bound="MachineCapabilities")


@_attrs_define
class MachineCapabilities:
    """
    Attributes:
        machine_id (str): Machine ID (mch_...).
        terminal (MachineTerminalCapability):
        desktop (MachineDesktopCapability):
        permissions (MachineInteractionPermissions):
        protocol_versions (MachineProtocolVersions):
    """

    machine_id: str
    terminal: "MachineTerminalCapability"
    desktop: "MachineDesktopCapability"
    permissions: "MachineInteractionPermissions"
    protocol_versions: "MachineProtocolVersions"

    def to_dict(self) -> dict[str, Any]:
        machine_id = self.machine_id

        terminal = self.terminal.to_dict()

        desktop = self.desktop.to_dict()

        permissions = self.permissions.to_dict()

        protocol_versions = self.protocol_versions.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine_id": machine_id,
                "terminal": terminal,
                "desktop": desktop,
                "permissions": permissions,
                "protocol_versions": protocol_versions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_desktop_capability import MachineDesktopCapability
        from ..models.machine_interaction_permissions import (
            MachineInteractionPermissions,
        )
        from ..models.machine_protocol_versions import MachineProtocolVersions
        from ..models.machine_terminal_capability import MachineTerminalCapability

        d = dict(src_dict)
        machine_id = d.pop("machine_id")

        terminal = MachineTerminalCapability.from_dict(d.pop("terminal"))

        desktop = MachineDesktopCapability.from_dict(d.pop("desktop"))

        permissions = MachineInteractionPermissions.from_dict(d.pop("permissions"))

        protocol_versions = MachineProtocolVersions.from_dict(
            d.pop("protocol_versions")
        )

        machine_capabilities = cls(
            machine_id=machine_id,
            terminal=terminal,
            desktop=desktop,
            permissions=permissions,
            protocol_versions=protocol_versions,
        )

        return machine_capabilities
