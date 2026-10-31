from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)
from uuid import UUID

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_reconciliation_claim import ProcessReconciliationClaim
    from ..models.register_daemon_runtime_request_capacity import (
        RegisterDaemonRuntimeRequestCapacity,
    )
    from ..models.register_daemon_runtime_request_observed_platform import (
        RegisterDaemonRuntimeRequestObservedPlatform,
    )


T = TypeVar("T", bound="RegisterDaemonRuntimeRequest")


@_attrs_define
class RegisterDaemonRuntimeRequest:
    """
    Attributes:
        daemon_instance_id (UUID):
        daemon_version (str):
        processes (list['ProcessReconciliationClaim']):
        capacity (Union[Unset, RegisterDaemonRuntimeRequestCapacity]):
        observed_platform (Union[Unset, RegisterDaemonRuntimeRequestObservedPlatform]):
    """

    daemon_instance_id: UUID
    daemon_version: str
    processes: list["ProcessReconciliationClaim"]
    capacity: Union[Unset, "RegisterDaemonRuntimeRequestCapacity"] = UNSET
    observed_platform: Union[Unset, "RegisterDaemonRuntimeRequestObservedPlatform"] = (
        UNSET
    )

    def to_dict(self) -> dict[str, Any]:
        daemon_instance_id = str(self.daemon_instance_id)

        daemon_version = self.daemon_version

        processes = []
        for processes_item_data in self.processes:
            processes_item = processes_item_data.to_dict()
            processes.append(processes_item)

        capacity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.capacity, Unset):
            capacity = self.capacity.to_dict()

        observed_platform: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.observed_platform, Unset):
            observed_platform = self.observed_platform.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "daemon_instance_id": daemon_instance_id,
                "daemon_version": daemon_version,
                "processes": processes,
            }
        )
        if capacity is not UNSET:
            field_dict["capacity"] = capacity
        if observed_platform is not UNSET:
            field_dict["observed_platform"] = observed_platform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_reconciliation_claim import ProcessReconciliationClaim
        from ..models.register_daemon_runtime_request_capacity import (
            RegisterDaemonRuntimeRequestCapacity,
        )
        from ..models.register_daemon_runtime_request_observed_platform import (
            RegisterDaemonRuntimeRequestObservedPlatform,
        )

        d = dict(src_dict)
        daemon_instance_id = UUID(d.pop("daemon_instance_id"))

        daemon_version = d.pop("daemon_version")

        processes = []
        _processes = d.pop("processes")
        for processes_item_data in _processes:
            processes_item = ProcessReconciliationClaim.from_dict(processes_item_data)

            processes.append(processes_item)

        _capacity = d.pop("capacity", UNSET)
        capacity: Union[Unset, RegisterDaemonRuntimeRequestCapacity]
        if isinstance(_capacity, Unset):
            capacity = UNSET
        else:
            capacity = RegisterDaemonRuntimeRequestCapacity.from_dict(_capacity)

        _observed_platform = d.pop("observed_platform", UNSET)
        observed_platform: Union[Unset, RegisterDaemonRuntimeRequestObservedPlatform]
        if isinstance(_observed_platform, Unset):
            observed_platform = UNSET
        else:
            observed_platform = RegisterDaemonRuntimeRequestObservedPlatform.from_dict(
                _observed_platform
            )

        register_daemon_runtime_request = cls(
            daemon_instance_id=daemon_instance_id,
            daemon_version=daemon_version,
            processes=processes,
            capacity=capacity,
            observed_platform=observed_platform,
        )

        return register_daemon_runtime_request
