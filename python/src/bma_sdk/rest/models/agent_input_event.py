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

from ..models.agent_control_type import AgentControlType, check_agent_control_type
from ..models.agent_input_event_event_kind import (
    AgentInputEventEventKind,
    check_agent_input_event_event_kind,
)
from ..models.agent_input_kind import AgentInputKind, check_agent_input_kind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_ref_content_block import MediaRefContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="AgentInputEvent")


@_attrs_define
class AgentInputEvent:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):
        turn_id (str):
        turn_sequence (int): Positive per-agent event, turn, or live-frame sequence.
        is_opening_event (bool):
        sequence (int): Positive per-agent event, turn, or live-frame sequence.
        event_kind (AgentInputEventEventKind):
        agent_input_id (str):
        input_kind (AgentInputKind):
        content_blocks (list[Union['MediaRefContentBlock', 'TextContentBlock']]):
        created_at (datetime.datetime):
        actor_id (Union[Unset, str]):
        input_idempotency_key (Union[Unset, str]): Echoes the Idempotency-Key of a content-input request so its sender
            can recognize the durable admission. Absent for other input kinds.
        control_type (Union[Unset, AgentControlType]):
        interaction_id (Union[Unset, str]):
        agent_config_id (Union[Unset, str]): Agent config ID (acfg_...).
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    turn_id: str
    turn_sequence: int
    is_opening_event: bool
    sequence: int
    event_kind: AgentInputEventEventKind
    agent_input_id: str
    input_kind: AgentInputKind
    content_blocks: list[Union["MediaRefContentBlock", "TextContentBlock"]]
    created_at: datetime.datetime
    actor_id: Union[Unset, str] = UNSET
    input_idempotency_key: Union[Unset, str] = UNSET
    control_type: Union[Unset, AgentControlType] = UNSET
    interaction_id: Union[Unset, str] = UNSET
    agent_config_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_content_block import TextContentBlock

        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        turn_id = self.turn_id

        turn_sequence = self.turn_sequence

        is_opening_event = self.is_opening_event

        sequence = self.sequence

        event_kind: str = self.event_kind

        agent_input_id = self.agent_input_id

        input_kind: str = self.input_kind

        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item: dict[str, Any]
            if isinstance(content_blocks_item_data, TextContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            else:
                content_blocks_item = content_blocks_item_data.to_dict()

            content_blocks.append(content_blocks_item)

        created_at = self.created_at.isoformat()

        actor_id = self.actor_id

        input_idempotency_key = self.input_idempotency_key

        control_type: Union[Unset, str] = UNSET
        if not isinstance(self.control_type, Unset):
            control_type = self.control_type

        interaction_id = self.interaction_id

        agent_config_id = self.agent_config_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "agent_id": agent_id,
                "turn_id": turn_id,
                "turn_sequence": turn_sequence,
                "is_opening_event": is_opening_event,
                "sequence": sequence,
                "event_kind": event_kind,
                "agent_input_id": agent_input_id,
                "input_kind": input_kind,
                "content_blocks": content_blocks,
                "created_at": created_at,
            }
        )
        if actor_id is not UNSET:
            field_dict["actor_id"] = actor_id
        if input_idempotency_key is not UNSET:
            field_dict["input_idempotency_key"] = input_idempotency_key
        if control_type is not UNSET:
            field_dict["control_type"] = control_type
        if interaction_id is not UNSET:
            field_dict["interaction_id"] = interaction_id
        if agent_config_id is not UNSET:
            field_dict["agent_config_id"] = agent_config_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        turn_id = d.pop("turn_id")

        turn_sequence = d.pop("turn_sequence")

        is_opening_event = d.pop("is_opening_event")

        sequence = d.pop("sequence")

        event_kind = check_agent_input_event_event_kind(d.pop("event_kind"))

        agent_input_id = d.pop("agent_input_id")

        input_kind = check_agent_input_kind(d.pop("input_kind"))

        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:

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

        created_at = isoparse(d.pop("created_at"))

        actor_id = d.pop("actor_id", UNSET)

        input_idempotency_key = d.pop("input_idempotency_key", UNSET)

        _control_type = d.pop("control_type", UNSET)
        control_type: Union[Unset, AgentControlType]
        if isinstance(_control_type, Unset):
            control_type = UNSET
        else:
            control_type = check_agent_control_type(_control_type)

        interaction_id = d.pop("interaction_id", UNSET)

        agent_config_id = d.pop("agent_config_id", UNSET)

        agent_input_event = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            turn_id=turn_id,
            turn_sequence=turn_sequence,
            is_opening_event=is_opening_event,
            sequence=sequence,
            event_kind=event_kind,
            agent_input_id=agent_input_id,
            input_kind=input_kind,
            content_blocks=content_blocks,
            created_at=created_at,
            actor_id=actor_id,
            input_idempotency_key=input_idempotency_key,
            control_type=control_type,
            interaction_id=interaction_id,
            agent_config_id=agent_config_id,
        )

        return agent_input_event
