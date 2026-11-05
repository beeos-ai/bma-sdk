import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config import AgentConfig
    from ..models.agent_profile_metadata import AgentProfileMetadata


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
        description (Union[None, Unset, str]): Caller-owned free-text description of the profile.
        metadata (Union[Unset, AgentProfileMetadata]): Caller-owned labels of an agent profile (string keys and values).
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
    description: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "AgentProfileMetadata"] = UNSET

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

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

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
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig
        from ..models.agent_profile_metadata import AgentProfileMetadata

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

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, AgentProfileMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = AgentProfileMetadata.from_dict(_metadata)

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
            description=description,
            metadata=metadata,
        )

        return agent_profile
