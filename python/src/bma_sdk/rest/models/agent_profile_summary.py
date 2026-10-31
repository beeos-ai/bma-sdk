import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_summary import AgentConfigSummary
    from ..models.agent_profile_stats import AgentProfileStats


T = TypeVar("T", bound="AgentProfileSummary")


@_attrs_define
class AgentProfileSummary:
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
        current_config (AgentConfigSummary):
        stats (Union[Unset, AgentProfileStats]): Present when the list was requested with `include_stats`.
    """

    id: str
    org_id: str
    project_id: str
    name: str
    current_config_id: str
    current_generation: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    current_config: "AgentConfigSummary"
    stats: Union[Unset, "AgentProfileStats"] = UNSET

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

        stats: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

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
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_summary import AgentConfigSummary
        from ..models.agent_profile_stats import AgentProfileStats

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        current_config_id = d.pop("current_config_id")

        current_generation = d.pop("current_generation")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        current_config = AgentConfigSummary.from_dict(d.pop("current_config"))

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, AgentProfileStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = AgentProfileStats.from_dict(_stats)

        agent_profile_summary = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            name=name,
            current_config_id=current_config_id,
            current_generation=current_generation,
            created_at=created_at,
            updated_at=updated_at,
            current_config=current_config,
            stats=stats,
        )

        return agent_profile_summary
