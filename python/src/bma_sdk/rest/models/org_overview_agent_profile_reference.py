from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="OrgOverviewAgentProfileReference")


@_attrs_define
class OrgOverviewAgentProfileReference:
    """
    Attributes:
        id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        agent_count (int): Agents, not counting subagents, launched from the profile, including archived ones.
    """

    id: str
    name: str
    agent_count: int

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        agent_count = self.agent_count

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "agent_count": agent_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        agent_count = d.pop("agent_count")

        org_overview_agent_profile_reference = cls(
            id=id,
            name=name,
            agent_count=agent_count,
        )

        return org_overview_agent_profile_reference
