from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.machine_connection_state import (
    MachineConnectionState,
    check_machine_connection_state,
)
from ..models.machine_power_state import MachinePowerState, check_machine_power_state

T = TypeVar("T", bound="MachinePowerStatus")


@_attrs_define
class MachinePowerStatus:
    """
    Attributes:
        machine_id (str): Machine ID (mch_...).
        connection_state (MachineConnectionState):
        power_state (MachinePowerState): Compute state of a pool machine. paused keeps the disk (and memory when the
            provider supports it) without compute; resuming means a resume or restore is in flight; archived means the
            machine image is stored durably and is restored on the next access.
    """

    machine_id: str
    connection_state: MachineConnectionState
    power_state: MachinePowerState

    def to_dict(self) -> dict[str, Any]:
        machine_id = self.machine_id

        connection_state: str = self.connection_state

        power_state: str = self.power_state

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine_id": machine_id,
                "connection_state": connection_state,
                "power_state": power_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        machine_id = d.pop("machine_id")

        connection_state = check_machine_connection_state(d.pop("connection_state"))

        power_state = check_machine_power_state(d.pop("power_state"))

        machine_power_status = cls(
            machine_id=machine_id,
            connection_state=connection_state,
            power_state=power_state,
        )

        return machine_power_status
