from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UpdateMachinePoolRequestDefaultMachineSecretEnv")


@_attrs_define
class UpdateMachinePoolRequestDefaultMachineSecretEnv:
    """Default secret environment for pool machines, mapping env names to generic secret references. References are
    resolved to secret values wherever the machine environment is applied.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        update_machine_pool_request_default_machine_secret_env = cls()

        update_machine_pool_request_default_machine_secret_env.additional_properties = d
        return update_machine_pool_request_default_machine_secret_env

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
