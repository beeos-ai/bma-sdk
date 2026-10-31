import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_machine_kind import AgentMachineKind, check_agent_machine_kind
from ..models.machine_connection_state import (
    MachineConnectionState,
    check_machine_connection_state,
)
from ..models.machine_lifecycle_state import (
    MachineLifecycleState,
    check_machine_lifecycle_state,
)

T = TypeVar("T", bound="AgentMachine")


@_attrs_define
class AgentMachine:
    """
    Attributes:
        id (str): Machine ID (mch_...).
        kind (AgentMachineKind): Persistent machines are kept for a person and never deleted for being idle; ephemeral
            machines serve turns and are deleted after their idle window.
        display_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        machine_pool_id (Union[None, str]):
        machine_pool_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace
            and invisible or control characters are not.
        lifecycle_state (MachineLifecycleState):
        connection_state (MachineConnectionState):
        cpu (Union[None, int]): The machine shape BMA reports, or null before the provider resolves it.
        memory_mb (Union[None, int]): The machine shape BMA reports, or null before the provider resolves it.
        created_at (datetime.datetime):
    """

    id: str
    kind: AgentMachineKind
    display_name: str
    machine_pool_id: Union[None, str]
    machine_pool_name: str
    lifecycle_state: MachineLifecycleState
    connection_state: MachineConnectionState
    cpu: Union[None, int]
    memory_mb: Union[None, int]
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        kind: str = self.kind

        display_name = self.display_name

        machine_pool_id: Union[None, str]
        machine_pool_id = self.machine_pool_id

        machine_pool_name = self.machine_pool_name

        lifecycle_state: str = self.lifecycle_state

        connection_state: str = self.connection_state

        cpu: Union[None, int]
        cpu = self.cpu

        memory_mb: Union[None, int]
        memory_mb = self.memory_mb

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "display_name": display_name,
                "machine_pool_id": machine_pool_id,
                "machine_pool_name": machine_pool_name,
                "lifecycle_state": lifecycle_state,
                "connection_state": connection_state,
                "cpu": cpu,
                "memory_mb": memory_mb,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        kind = check_agent_machine_kind(d.pop("kind"))

        display_name = d.pop("display_name")

        def _parse_machine_pool_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        machine_pool_id = _parse_machine_pool_id(d.pop("machine_pool_id"))

        machine_pool_name = d.pop("machine_pool_name")

        lifecycle_state = check_machine_lifecycle_state(d.pop("lifecycle_state"))

        connection_state = check_machine_connection_state(d.pop("connection_state"))

        def _parse_cpu(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cpu = _parse_cpu(d.pop("cpu"))

        def _parse_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb"))

        created_at = isoparse(d.pop("created_at"))

        agent_machine = cls(
            id=id,
            kind=kind,
            display_name=display_name,
            machine_pool_id=machine_pool_id,
            machine_pool_name=machine_pool_name,
            lifecycle_state=lifecycle_state,
            connection_state=connection_state,
            cpu=cpu,
            memory_mb=memory_mb,
            created_at=created_at,
        )

        return agent_machine
