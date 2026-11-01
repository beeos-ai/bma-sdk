from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentExecutorBindingInput")


@_attrs_define
class AgentExecutorBindingInput:
    """
    Attributes:
        machine_id (str): Machine ID (mch_...).
    """

    machine_id: str

    def to_dict(self) -> dict[str, Any]:
        machine_id = self.machine_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine_id": machine_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        machine_id = d.pop("machine_id")

        agent_executor_binding_input = cls(
            machine_id=machine_id,
        )

        return agent_executor_binding_input
