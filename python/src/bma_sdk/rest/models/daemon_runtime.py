import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.daemon_runtime_state import DaemonRuntimeState, check_daemon_runtime_state

if TYPE_CHECKING:
    from ..models.daemon_runtime_capacity import DaemonRuntimeCapacity


T = TypeVar("T", bound="DaemonRuntime")


@_attrs_define
class DaemonRuntime:
    """
    Attributes:
        id (str):
        org_id (str):
        machine_id (str): Machine ID (mch_...).
        daemon_instance_id (UUID):
        daemon_version (str):
        state (DaemonRuntimeState):
        state_reason_code (str):
        state_reason_message (str):
        created_at (datetime.datetime):
        last_seen_at (datetime.datetime):
        lease_expires_at (datetime.datetime):
        next_heartbeat_after_ms (int):
        ended_at (Union[None, datetime.datetime]):
        capacity (DaemonRuntimeCapacity):
    """

    id: str
    org_id: str
    machine_id: str
    daemon_instance_id: UUID
    daemon_version: str
    state: DaemonRuntimeState
    state_reason_code: str
    state_reason_message: str
    created_at: datetime.datetime
    last_seen_at: datetime.datetime
    lease_expires_at: datetime.datetime
    next_heartbeat_after_ms: int
    ended_at: Union[None, datetime.datetime]
    capacity: "DaemonRuntimeCapacity"

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        machine_id = self.machine_id

        daemon_instance_id = str(self.daemon_instance_id)

        daemon_version = self.daemon_version

        state: str = self.state

        state_reason_code = self.state_reason_code

        state_reason_message = self.state_reason_message

        created_at = self.created_at.isoformat()

        last_seen_at = self.last_seen_at.isoformat()

        lease_expires_at = self.lease_expires_at.isoformat()

        next_heartbeat_after_ms = self.next_heartbeat_after_ms

        ended_at: Union[None, str]
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        capacity = self.capacity.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "machine_id": machine_id,
                "daemon_instance_id": daemon_instance_id,
                "daemon_version": daemon_version,
                "state": state,
                "state_reason_code": state_reason_code,
                "state_reason_message": state_reason_message,
                "created_at": created_at,
                "last_seen_at": last_seen_at,
                "lease_expires_at": lease_expires_at,
                "next_heartbeat_after_ms": next_heartbeat_after_ms,
                "ended_at": ended_at,
                "capacity": capacity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daemon_runtime_capacity import DaemonRuntimeCapacity

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        machine_id = d.pop("machine_id")

        daemon_instance_id = UUID(d.pop("daemon_instance_id"))

        daemon_version = d.pop("daemon_version")

        state = check_daemon_runtime_state(d.pop("state"))

        state_reason_code = d.pop("state_reason_code")

        state_reason_message = d.pop("state_reason_message")

        created_at = isoparse(d.pop("created_at"))

        last_seen_at = isoparse(d.pop("last_seen_at"))

        lease_expires_at = isoparse(d.pop("lease_expires_at"))

        next_heartbeat_after_ms = d.pop("next_heartbeat_after_ms")

        def _parse_ended_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = isoparse(data)

                return ended_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        capacity = DaemonRuntimeCapacity.from_dict(d.pop("capacity"))

        daemon_runtime = cls(
            id=id,
            org_id=org_id,
            machine_id=machine_id,
            daemon_instance_id=daemon_instance_id,
            daemon_version=daemon_version,
            state=state,
            state_reason_code=state_reason_code,
            state_reason_message=state_reason_message,
            created_at=created_at,
            last_seen_at=last_seen_at,
            lease_expires_at=lease_expires_at,
            next_heartbeat_after_ms=next_heartbeat_after_ms,
            ended_at=ended_at,
            capacity=capacity,
        )

        return daemon_runtime
