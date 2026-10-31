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

from ..models.agent_state import AgentState, check_agent_state
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_activity import AgentActivity
    from ..models.agent_model import AgentModel
    from ..models.integration_target import IntegrationTarget
    from ..models.usage_totals import UsageTotals


T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        state (AgentState):
        name (str): Agent name. Empty means the agent is unnamed; non-empty values use the ResourceName policy.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        agent_profile_id (Union[Unset, str]):
        integration_target (Union[Unset, IntegrationTarget]):
        current_config_id (Union[Unset, str]): Agent config ID (acfg_...).
        model (Union[Unset, AgentModel]):
        parent_agent_id (Union[Unset, str]):
        subagent_key (Union[Unset, str]): The `subagents` key this agent was spawned from.
        activity (Union[Unset, AgentActivity]):
        usage (Union[Unset, UsageTotals]):
        archived_at (Union[Unset, datetime.datetime]):
    """

    id: str
    org_id: str
    project_id: str
    state: AgentState
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    agent_profile_id: Union[Unset, str] = UNSET
    integration_target: Union[Unset, "IntegrationTarget"] = UNSET
    current_config_id: Union[Unset, str] = UNSET
    model: Union[Unset, "AgentModel"] = UNSET
    parent_agent_id: Union[Unset, str] = UNSET
    subagent_key: Union[Unset, str] = UNSET
    activity: Union[Unset, "AgentActivity"] = UNSET
    usage: Union[Unset, "UsageTotals"] = UNSET
    archived_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        state: str = self.state

        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        agent_profile_id = self.agent_profile_id

        integration_target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.integration_target, Unset):
            integration_target = self.integration_target.to_dict()

        current_config_id = self.current_config_id

        model: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        parent_agent_id = self.parent_agent_id

        subagent_key = self.subagent_key

        activity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.activity, Unset):
            activity = self.activity.to_dict()

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        archived_at: Union[Unset, str] = UNSET
        if not isinstance(self.archived_at, Unset):
            archived_at = self.archived_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "state": state,
                "name": name,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if agent_profile_id is not UNSET:
            field_dict["agent_profile_id"] = agent_profile_id
        if integration_target is not UNSET:
            field_dict["integration_target"] = integration_target
        if current_config_id is not UNSET:
            field_dict["current_config_id"] = current_config_id
        if model is not UNSET:
            field_dict["model"] = model
        if parent_agent_id is not UNSET:
            field_dict["parent_agent_id"] = parent_agent_id
        if subagent_key is not UNSET:
            field_dict["subagent_key"] = subagent_key
        if activity is not UNSET:
            field_dict["activity"] = activity
        if usage is not UNSET:
            field_dict["usage"] = usage
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_activity import AgentActivity
        from ..models.agent_model import AgentModel
        from ..models.integration_target import IntegrationTarget
        from ..models.usage_totals import UsageTotals

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        state = check_agent_state(d.pop("state"))

        name = d.pop("name")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        agent_profile_id = d.pop("agent_profile_id", UNSET)

        _integration_target = d.pop("integration_target", UNSET)
        integration_target: Union[Unset, IntegrationTarget]
        if isinstance(_integration_target, Unset):
            integration_target = UNSET
        else:
            integration_target = IntegrationTarget.from_dict(_integration_target)

        current_config_id = d.pop("current_config_id", UNSET)

        _model = d.pop("model", UNSET)
        model: Union[Unset, AgentModel]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = AgentModel.from_dict(_model)

        parent_agent_id = d.pop("parent_agent_id", UNSET)

        subagent_key = d.pop("subagent_key", UNSET)

        _activity = d.pop("activity", UNSET)
        activity: Union[Unset, AgentActivity]
        if isinstance(_activity, Unset):
            activity = UNSET
        else:
            activity = AgentActivity.from_dict(_activity)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, UsageTotals]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = UsageTotals.from_dict(_usage)

        _archived_at = d.pop("archived_at", UNSET)
        archived_at: Union[Unset, datetime.datetime]
        if isinstance(_archived_at, Unset):
            archived_at = UNSET
        else:
            archived_at = isoparse(_archived_at)

        agent = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            state=state,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            agent_profile_id=agent_profile_id,
            integration_target=integration_target,
            current_config_id=current_config_id,
            model=model,
            parent_agent_id=parent_agent_id,
            subagent_key=subagent_key,
            activity=activity,
            usage=usage,
            archived_at=archived_at,
        )

        return agent
