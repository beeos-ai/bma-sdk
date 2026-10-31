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

from ..models.agent_config_summary_source_format import (
    AgentConfigSummarySourceFormat,
    check_agent_config_summary_source_format,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_model import AgentConfigModel


T = TypeVar("T", bound="AgentConfigSummary")


@_attrs_define
class AgentConfigSummary:
    """
    Attributes:
        id (str): Agent config ID (acfg_...).
        org_id (str):
        project_id (str): Project ID (proj_...).
        effective_definition_hash (str):
        model (AgentConfigModel):
        created_at (datetime.datetime):
        source (Union[Unset, str]):
        source_format (Union[Unset, AgentConfigSummarySourceFormat]):
        instruction_hash (Union[Unset, str]):
    """

    id: str
    org_id: str
    project_id: str
    effective_definition_hash: str
    model: "AgentConfigModel"
    created_at: datetime.datetime
    source: Union[Unset, str] = UNSET
    source_format: Union[Unset, AgentConfigSummarySourceFormat] = UNSET
    instruction_hash: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        effective_definition_hash = self.effective_definition_hash

        model = self.model.to_dict()

        created_at = self.created_at.isoformat()

        source = self.source

        source_format: Union[Unset, str] = UNSET
        if not isinstance(self.source_format, Unset):
            source_format = self.source_format

        instruction_hash = self.instruction_hash

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "effective_definition_hash": effective_definition_hash,
                "model": model,
                "created_at": created_at,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if source_format is not UNSET:
            field_dict["source_format"] = source_format
        if instruction_hash is not UNSET:
            field_dict["instruction_hash"] = instruction_hash

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_model import AgentConfigModel

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        effective_definition_hash = d.pop("effective_definition_hash")

        model = AgentConfigModel.from_dict(d.pop("model"))

        created_at = isoparse(d.pop("created_at"))

        source = d.pop("source", UNSET)

        _source_format = d.pop("source_format", UNSET)
        source_format: Union[Unset, AgentConfigSummarySourceFormat]
        if isinstance(_source_format, Unset):
            source_format = UNSET
        else:
            source_format = check_agent_config_summary_source_format(_source_format)

        instruction_hash = d.pop("instruction_hash", UNSET)

        agent_config_summary = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            effective_definition_hash=effective_definition_hash,
            model=model,
            created_at=created_at,
            source=source,
            source_format=source_format,
            instruction_hash=instruction_hash,
        )

        return agent_config_summary
