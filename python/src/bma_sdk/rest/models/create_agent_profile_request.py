from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_profile_metadata import AgentProfileMetadata


T = TypeVar("T", bound="CreateAgentProfileRequest")


@_attrs_define
class CreateAgentProfileRequest:
    """
    Attributes:
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        config (str): Agent config ID (acfg_...).
        description (Union[None, Unset, str]): Caller-owned free-text description of the profile.
        metadata (Union[Unset, AgentProfileMetadata]): Caller-owned labels of an agent profile (string keys and values).
    """

    name: str
    config: str
    description: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "AgentProfileMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        config = self.config

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
                "name": name,
                "config": config,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_profile_metadata import AgentProfileMetadata

        d = dict(src_dict)
        name = d.pop("name")

        config = d.pop("config")

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

        create_agent_profile_request = cls(
            name=name,
            config=config,
            description=description,
            metadata=metadata,
        )

        return create_agent_profile_request
