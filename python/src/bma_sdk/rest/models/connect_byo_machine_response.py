from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine import Machine
    from ..models.machine_daemon_token import MachineDaemonToken
    from ..models.project_machine_grant import ProjectMachineGrant


T = TypeVar("T", bound="ConnectBYOMachineResponse")


@_attrs_define
class ConnectBYOMachineResponse:
    """
    Attributes:
        machine (Machine):
        token (str): Opaque bearer credential.
        token_record (MachineDaemonToken):
        project_grants (list['ProjectMachineGrant']):
    """

    machine: "Machine"
    token: str
    token_record: "MachineDaemonToken"
    project_grants: list["ProjectMachineGrant"]

    def to_dict(self) -> dict[str, Any]:
        machine = self.machine.to_dict()

        token = self.token

        token_record = self.token_record.to_dict()

        project_grants = []
        for project_grants_item_data in self.project_grants:
            project_grants_item = project_grants_item_data.to_dict()
            project_grants.append(project_grants_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine": machine,
                "token": token,
                "token_record": token_record,
                "project_grants": project_grants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine import Machine
        from ..models.machine_daemon_token import MachineDaemonToken
        from ..models.project_machine_grant import ProjectMachineGrant

        d = dict(src_dict)
        machine = Machine.from_dict(d.pop("machine"))

        token = d.pop("token")

        token_record = MachineDaemonToken.from_dict(d.pop("token_record"))

        project_grants = []
        _project_grants = d.pop("project_grants")
        for project_grants_item_data in _project_grants:
            project_grants_item = ProjectMachineGrant.from_dict(
                project_grants_item_data
            )

            project_grants.append(project_grants_item)

        connect_byo_machine_response = cls(
            machine=machine,
            token=token,
            token_record=token_record,
            project_grants=project_grants,
        )

        return connect_byo_machine_response
