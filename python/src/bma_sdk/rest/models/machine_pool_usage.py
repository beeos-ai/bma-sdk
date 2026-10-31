from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MachinePoolUsage")


@_attrs_define
class MachinePoolUsage:
    """
    Attributes:
        machines (int):
        cpu (int):
        memory_mb (int):
    """

    machines: int
    cpu: int
    memory_mb: int

    def to_dict(self) -> dict[str, Any]:
        machines = self.machines

        cpu = self.cpu

        memory_mb = self.memory_mb

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machines": machines,
                "cpu": cpu,
                "memory_mb": memory_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        machines = d.pop("machines")

        cpu = d.pop("cpu")

        memory_mb = d.pop("memory_mb")

        machine_pool_usage = cls(
            machines=machines,
            cpu=cpu,
            memory_mb=memory_mb,
        )

        return machine_pool_usage
