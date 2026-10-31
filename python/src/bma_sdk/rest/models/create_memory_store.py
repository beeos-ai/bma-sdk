from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.memory_store_access import MemoryStoreAccess, check_memory_store_access
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateMemoryStore")


@_attrs_define
class CreateMemoryStore:
    """
    Attributes:
        name (str): Machine-readable memory store identifier consisting of lowercase ASCII segments separated by single
            hyphens.
        description (Union[Unset, str]):
        agent_access (Union[Unset, MemoryStoreAccess]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    agent_access: Union[Unset, MemoryStoreAccess] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        agent_access: Union[Unset, str] = UNSET
        if not isinstance(self.agent_access, Unset):
            agent_access = self.agent_access

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if agent_access is not UNSET:
            field_dict["agent_access"] = agent_access

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        _agent_access = d.pop("agent_access", UNSET)
        agent_access: Union[Unset, MemoryStoreAccess]
        if isinstance(_agent_access, Unset):
            agent_access = UNSET
        else:
            agent_access = check_memory_store_access(_agent_access)

        create_memory_store = cls(
            name=name,
            description=description,
            agent_access=agent_access,
        )

        return create_memory_store
