from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateMachinePoolRequestBaseDefaultMachineEnv")


@_attrs_define
class CreateMachinePoolRequestBaseDefaultMachineEnv:
    """Default environment for pool machines. A machine's environment, including resolved secret_env values, is applied to
    the provider machine at provisioning, so the provider_options startup_script and the daemon run with it, and is
    resolved again for each process at launch.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create_machine_pool_request_base_default_machine_env = cls()

        create_machine_pool_request_base_default_machine_env.additional_properties = d
        return create_machine_pool_request_base_default_machine_env

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
