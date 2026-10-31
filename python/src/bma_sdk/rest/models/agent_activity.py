import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_activity_state import AgentActivityState, check_agent_activity_state

T = TypeVar("T", bound="AgentActivity")


@_attrs_define
class AgentActivity:
    """
    Attributes:
        state (AgentActivityState): running while the agent has work in progress, which includes a custom tool call
            awaiting its result; waiting_on_interaction while it has an open question or permission request; idle otherwise;
            and archived once the agent is archived.
        last_activity_at (datetime.datetime):
    """

    state: AgentActivityState
    last_activity_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        state: str = self.state

        last_activity_at = self.last_activity_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "state": state,
                "last_activity_at": last_activity_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = check_agent_activity_state(d.pop("state"))

        last_activity_at = isoparse(d.pop("last_activity_at"))

        agent_activity = cls(
            state=state,
            last_activity_at=last_activity_at,
        )

        return agent_activity
