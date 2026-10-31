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

from ..models.agent_input_delivery_mode import (
    AgentInputDeliveryMode,
    check_agent_input_delivery_mode,
)
from ..models.agent_input_kind import AgentInputKind, check_agent_input_kind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_ref_content_block import MediaRefContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="AgentInput")


@_attrs_define
class AgentInput:
    """
    Attributes:
        id (str):
        agent_id (str):
        state (str):
        delivery_mode (AgentInputDeliveryMode):
        input_kind (AgentInputKind):
        queued_at (datetime.datetime):
        actor_id (Union[Unset, str]):
        input_idempotency_key (Union[Unset, str]): Idempotency key supplied when this content input was created. Absent
            for other input kinds.
        content_blocks (Union[Unset, list[Union['MediaRefContentBlock', 'TextContentBlock']]]):
    """

    id: str
    agent_id: str
    state: str
    delivery_mode: AgentInputDeliveryMode
    input_kind: AgentInputKind
    queued_at: datetime.datetime
    actor_id: Union[Unset, str] = UNSET
    input_idempotency_key: Union[Unset, str] = UNSET
    content_blocks: Union[
        Unset, list[Union["MediaRefContentBlock", "TextContentBlock"]]
    ] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_content_block import TextContentBlock

        id = self.id

        agent_id = self.agent_id

        state = self.state

        delivery_mode: str = self.delivery_mode

        input_kind: str = self.input_kind

        queued_at = self.queued_at.isoformat()

        actor_id = self.actor_id

        input_idempotency_key = self.input_idempotency_key

        content_blocks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.content_blocks, Unset):
            content_blocks = []
            for content_blocks_item_data in self.content_blocks:
                content_blocks_item: dict[str, Any]
                if isinstance(content_blocks_item_data, TextContentBlock):
                    content_blocks_item = content_blocks_item_data.to_dict()
                else:
                    content_blocks_item = content_blocks_item_data.to_dict()

                content_blocks.append(content_blocks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "agent_id": agent_id,
                "state": state,
                "delivery_mode": delivery_mode,
                "input_kind": input_kind,
                "queued_at": queued_at,
            }
        )
        if actor_id is not UNSET:
            field_dict["actor_id"] = actor_id
        if input_idempotency_key is not UNSET:
            field_dict["input_idempotency_key"] = input_idempotency_key
        if content_blocks is not UNSET:
            field_dict["content_blocks"] = content_blocks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        id = d.pop("id")

        agent_id = d.pop("agent_id")

        state = d.pop("state")

        delivery_mode = check_agent_input_delivery_mode(d.pop("delivery_mode"))

        input_kind = check_agent_input_kind(d.pop("input_kind"))

        queued_at = isoparse(d.pop("queued_at"))

        actor_id = d.pop("actor_id", UNSET)

        input_idempotency_key = d.pop("input_idempotency_key", UNSET)

        content_blocks = []
        _content_blocks = d.pop("content_blocks", UNSET)
        for content_blocks_item_data in _content_blocks or []:

            def _parse_content_blocks_item(
                data: object,
            ) -> Union["MediaRefContentBlock", "TextContentBlock"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_agent_input_content_block_type_0 = (
                        TextContentBlock.from_dict(data)
                    )

                    return componentsschemas_agent_input_content_block_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_input_content_block_type_1 = (
                    MediaRefContentBlock.from_dict(data)
                )

                return componentsschemas_agent_input_content_block_type_1

            content_blocks_item = _parse_content_blocks_item(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        agent_input = cls(
            id=id,
            agent_id=agent_id,
            state=state,
            delivery_mode=delivery_mode,
            input_kind=input_kind,
            queued_at=queued_at,
            actor_id=actor_id,
            input_idempotency_key=input_idempotency_key,
            content_blocks=content_blocks,
        )

        return agent_input
