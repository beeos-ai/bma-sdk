from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAgentPersistentMachineRequest")


@_attrs_define
class CreateAgentPersistentMachineRequest:
    """
    Attributes:
        template (str): The sold machine-class template (for example base-2c4g, base-2c8g or base-8c32g). It must be
            allowed by the machine pool's provider configuration.
        machine_pool_id (Union[Unset, str]): Machine pool ID (mpo_...).
        display_name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
    """

    template: str
    machine_pool_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        template = self.template

        machine_pool_id = self.machine_pool_id

        display_name = self.display_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "template": template,
            }
        )
        if machine_pool_id is not UNSET:
            field_dict["machine_pool_id"] = machine_pool_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template = d.pop("template")

        machine_pool_id = d.pop("machine_pool_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        create_agent_persistent_machine_request = cls(
            template=template,
            machine_pool_id=machine_pool_id,
            display_name=display_name,
        )

        return create_agent_persistent_machine_request
