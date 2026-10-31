from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent import Agent
    from ..models.agent_profile_summary import AgentProfileSummary
    from ..models.org_overview_agent_profile_reference import (
        OrgOverviewAgentProfileReference,
    )
    from ..models.org_overview_project_activity import OrgOverviewProjectActivity
    from ..models.visible_project import VisibleProject


T = TypeVar("T", bound="OrgOverviewResponse")


@_attrs_define
class OrgOverviewResponse:
    """
    Attributes:
        projects (list['VisibleProject']): Projects visible to the caller, most recently active first, capped at 200.
            Recents and activity still cover every visible project.
        project_activity (list['OrgOverviewProjectActivity']): When each listed project last had an active top-level
            agent or an agent profile updated, among those the caller can read. Projects with neither are omitted.
        recent_agents (list['Agent']): Most recently active agents across the caller's readable projects, ordered by
            updated_at descending.
        recent_agent_profiles (list['AgentProfileSummary']): Most recently updated agent profiles across the caller's
            readable projects, ordered by updated_at descending.
        referenced_agent_profiles (list['OrgOverviewAgentProfileReference']): The agent profiles that recent_agents and
            recent_agent_profiles reference, with how many agents were launched from each. Profiles since deleted are
            omitted.
    """

    projects: list["VisibleProject"]
    project_activity: list["OrgOverviewProjectActivity"]
    recent_agents: list["Agent"]
    recent_agent_profiles: list["AgentProfileSummary"]
    referenced_agent_profiles: list["OrgOverviewAgentProfileReference"]

    def to_dict(self) -> dict[str, Any]:
        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()
            projects.append(projects_item)

        project_activity = []
        for project_activity_item_data in self.project_activity:
            project_activity_item = project_activity_item_data.to_dict()
            project_activity.append(project_activity_item)

        recent_agents = []
        for recent_agents_item_data in self.recent_agents:
            recent_agents_item = recent_agents_item_data.to_dict()
            recent_agents.append(recent_agents_item)

        recent_agent_profiles = []
        for recent_agent_profiles_item_data in self.recent_agent_profiles:
            recent_agent_profiles_item = recent_agent_profiles_item_data.to_dict()
            recent_agent_profiles.append(recent_agent_profiles_item)

        referenced_agent_profiles = []
        for referenced_agent_profiles_item_data in self.referenced_agent_profiles:
            referenced_agent_profiles_item = (
                referenced_agent_profiles_item_data.to_dict()
            )
            referenced_agent_profiles.append(referenced_agent_profiles_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "projects": projects,
                "project_activity": project_activity,
                "recent_agents": recent_agents,
                "recent_agent_profiles": recent_agent_profiles,
                "referenced_agent_profiles": referenced_agent_profiles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent import Agent
        from ..models.agent_profile_summary import AgentProfileSummary
        from ..models.org_overview_agent_profile_reference import (
            OrgOverviewAgentProfileReference,
        )
        from ..models.org_overview_project_activity import OrgOverviewProjectActivity
        from ..models.visible_project import VisibleProject

        d = dict(src_dict)
        projects = []
        _projects = d.pop("projects")
        for projects_item_data in _projects:
            projects_item = VisibleProject.from_dict(projects_item_data)

            projects.append(projects_item)

        project_activity = []
        _project_activity = d.pop("project_activity")
        for project_activity_item_data in _project_activity:
            project_activity_item = OrgOverviewProjectActivity.from_dict(
                project_activity_item_data
            )

            project_activity.append(project_activity_item)

        recent_agents = []
        _recent_agents = d.pop("recent_agents")
        for recent_agents_item_data in _recent_agents:
            recent_agents_item = Agent.from_dict(recent_agents_item_data)

            recent_agents.append(recent_agents_item)

        recent_agent_profiles = []
        _recent_agent_profiles = d.pop("recent_agent_profiles")
        for recent_agent_profiles_item_data in _recent_agent_profiles:
            recent_agent_profiles_item = AgentProfileSummary.from_dict(
                recent_agent_profiles_item_data
            )

            recent_agent_profiles.append(recent_agent_profiles_item)

        referenced_agent_profiles = []
        _referenced_agent_profiles = d.pop("referenced_agent_profiles")
        for referenced_agent_profiles_item_data in _referenced_agent_profiles:
            referenced_agent_profiles_item = OrgOverviewAgentProfileReference.from_dict(
                referenced_agent_profiles_item_data
            )

            referenced_agent_profiles.append(referenced_agent_profiles_item)

        org_overview_response = cls(
            projects=projects,
            project_activity=project_activity,
            recent_agents=recent_agents,
            recent_agent_profiles=recent_agent_profiles,
            referenced_agent_profiles=referenced_agent_profiles,
        )

        return org_overview_response
