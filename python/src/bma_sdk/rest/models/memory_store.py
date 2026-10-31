import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.memory_store_access import MemoryStoreAccess, check_memory_store_access

T = TypeVar("T", bound="MemoryStore")


@_attrs_define
class MemoryStore:
    """
    Attributes:
        id (str):
        project_id (str): Project ID (proj_...).
        name (str): Machine-readable memory store identifier consisting of lowercase ASCII segments separated by single
            hyphens.
        description (str):
        agent_access (MemoryStoreAccess):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    project_id: str
    name: str
    description: str
    agent_access: MemoryStoreAccess
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        name = self.name

        description = self.description

        agent_access: str = self.agent_access

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "name": name,
                "description": description,
                "agent_access": agent_access,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        description = d.pop("description")

        agent_access = check_memory_store_access(d.pop("agent_access"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        memory_store = cls(
            id=id,
            project_id=project_id,
            name=name,
            description=description,
            agent_access=agent_access,
            created_at=created_at,
            updated_at=updated_at,
        )

        return memory_store
