import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.agent_config import AgentConfig


T = TypeVar("T", bound="AgentProfile")


@_attrs_define
class AgentProfile:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        current_config_id (str): Agent config ID (acfg_...).
        current_generation (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        current_config (AgentConfig):
    """

    id: str
    org_id: str
    project_id: str
    name: str
    current_config_id: str
    current_generation: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    current_config: "AgentConfig"

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        name = self.name

        current_config_id = self.current_config_id

        current_generation = self.current_generation

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        current_config = self.current_config.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "name": name,
                "current_config_id": current_config_id,
                "current_generation": current_generation,
                "created_at": created_at,
                "updated_at": updated_at,
                "current_config": current_config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        current_config_id = d.pop("current_config_id")

        current_generation = d.pop("current_generation")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        current_config = AgentConfig.from_dict(d.pop("current_config"))

        agent_profile = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            name=name,
            current_config_id=current_config_id,
            current_generation=current_generation,
            created_at=created_at,
            updated_at=updated_at,
            current_config=current_config,
        )

        return agent_profile
