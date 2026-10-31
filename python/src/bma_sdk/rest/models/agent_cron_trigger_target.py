from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_cron_trigger_target_type import (
    AgentCronTriggerTargetType,
    check_agent_cron_trigger_target_type,
)
from ..models.cron_trigger_delivery_mode import (
    CronTriggerDeliveryMode,
    check_cron_trigger_delivery_mode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentCronTriggerTarget")


@_attrs_define
class AgentCronTriggerTarget:
    """
    Attributes:
        type_ (AgentCronTriggerTargetType):
        agent_id (str):
        delivery_mode (Union[Unset, CronTriggerDeliveryMode]): Each firing sends a queued or steering message to the
            agent. Defaults to `queued` on creation; omitted updates preserve the current mode.
    """

    type_: AgentCronTriggerTargetType
    agent_id: str
    delivery_mode: Union[Unset, CronTriggerDeliveryMode] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        agent_id = self.agent_id

        delivery_mode: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_mode, Unset):
            delivery_mode = self.delivery_mode

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "agent_id": agent_id,
            }
        )
        if delivery_mode is not UNSET:
            field_dict["delivery_mode"] = delivery_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_agent_cron_trigger_target_type(d.pop("type"))

        agent_id = d.pop("agent_id")

        _delivery_mode = d.pop("delivery_mode", UNSET)
        delivery_mode: Union[Unset, CronTriggerDeliveryMode]
        if isinstance(_delivery_mode, Unset):
            delivery_mode = UNSET
        else:
            delivery_mode = check_cron_trigger_delivery_mode(_delivery_mode)

        agent_cron_trigger_target = cls(
            type_=type_,
            agent_id=agent_id,
            delivery_mode=delivery_mode,
        )

        return agent_cron_trigger_target
