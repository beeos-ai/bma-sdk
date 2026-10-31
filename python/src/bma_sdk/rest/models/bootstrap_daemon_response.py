from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="BootstrapDaemonResponse")


@_attrs_define
class BootstrapDaemonResponse:
    """
    Attributes:
        installation_id (str):
        machine_id (str): Machine ID (mch_...).
    """

    installation_id: str
    machine_id: str

    def to_dict(self) -> dict[str, Any]:
        installation_id = self.installation_id

        machine_id = self.machine_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "installation_id": installation_id,
                "machine_id": machine_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        installation_id = d.pop("installation_id")

        machine_id = d.pop("machine_id")

        bootstrap_daemon_response = cls(
            installation_id=installation_id,
            machine_id=machine_id,
        )

        return bootstrap_daemon_response
