from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.usage_totals import UsageTotals


T = TypeVar("T", bound="AgentProfileStats")


@_attrs_define
class AgentProfileStats:
    """Present when the list was requested with `include_stats`.

    Attributes:
        agent_count (int): Unarchived top-level agents launched from the profile.
        usage (UsageTotals):
    """

    agent_count: int
    usage: "UsageTotals"

    def to_dict(self) -> dict[str, Any]:
        agent_count = self.agent_count

        usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_count": agent_count,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_totals import UsageTotals

        d = dict(src_dict)
        agent_count = d.pop("agent_count")

        usage = UsageTotals.from_dict(d.pop("usage"))

        agent_profile_stats = cls(
            agent_count=agent_count,
            usage=usage,
        )

        return agent_profile_stats
