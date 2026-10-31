import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)
from uuid import UUID

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.desktop_capabilities import DesktopCapabilities
    from ..models.desktop_control_status import DesktopControlStatus


T = TypeVar("T", bound="DesktopSession")


@_attrs_define
class DesktopSession:
    """
    Attributes:
        id (str): Desktop session ID (dsn_...).
        org_id (str):
        project_id (str): Project ID (proj_...).
        machine_id (str): Machine ID (mch_...).
        owner_id (UUID): Authenticated user or organization API key that created the session.
        read_only (bool):
        closed (bool):
        created_at (datetime.datetime):
        capabilities (DesktopCapabilities):
        control (DesktopControlStatus):
        agent_id (Union[Unset, str]):
    """

    id: str
    org_id: str
    project_id: str
    machine_id: str
    owner_id: UUID
    read_only: bool
    closed: bool
    created_at: datetime.datetime
    capabilities: "DesktopCapabilities"
    control: "DesktopControlStatus"
    agent_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        machine_id = self.machine_id

        owner_id = str(self.owner_id)

        read_only = self.read_only

        closed = self.closed

        created_at = self.created_at.isoformat()

        capabilities = self.capabilities.to_dict()

        control = self.control.to_dict()

        agent_id = self.agent_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "machine_id": machine_id,
                "owner_id": owner_id,
                "read_only": read_only,
                "closed": closed,
                "created_at": created_at,
                "capabilities": capabilities,
                "control": control,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.desktop_capabilities import DesktopCapabilities
        from ..models.desktop_control_status import DesktopControlStatus

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        machine_id = d.pop("machine_id")

        owner_id = UUID(d.pop("owner_id"))

        read_only = d.pop("read_only")

        closed = d.pop("closed")

        created_at = isoparse(d.pop("created_at"))

        capabilities = DesktopCapabilities.from_dict(d.pop("capabilities"))

        control = DesktopControlStatus.from_dict(d.pop("control"))

        agent_id = d.pop("agent_id", UNSET)

        desktop_session = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            owner_id=owner_id,
            read_only=read_only,
            closed=closed,
            created_at=created_at,
            capabilities=capabilities,
            control=control,
            agent_id=agent_id,
        )

        return desktop_session
