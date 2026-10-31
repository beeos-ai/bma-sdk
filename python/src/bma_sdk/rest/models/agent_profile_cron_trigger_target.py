from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_profile_cron_trigger_target_type import (
    AgentProfileCronTriggerTargetType,
    check_agent_profile_cron_trigger_target_type,
)

T = TypeVar("T", bound="AgentProfileCronTriggerTarget")


@_attrs_define
class AgentProfileCronTriggerTarget:
    """
    Attributes:
        type_ (AgentProfileCronTriggerTargetType):
        agent_profile_id (str):
    """

    type_: AgentProfileCronTriggerTargetType
    agent_profile_id: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        agent_profile_id = self.agent_profile_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "agent_profile_id": agent_profile_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_agent_profile_cron_trigger_target_type(d.pop("type"))

        agent_profile_id = d.pop("agent_profile_id")

        agent_profile_cron_trigger_target = cls(
            type_=type_,
            agent_profile_id=agent_profile_id,
        )

        return agent_profile_cron_trigger_target
