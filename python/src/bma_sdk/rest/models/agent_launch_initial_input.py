from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.external_actor_params import ExternalActorParams
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="AgentLaunchInitialInput")


@_attrs_define
class AgentLaunchInitialInput:
    """Initial queued text input, committed atomically with the agent and any derived config. Mutually exclusive with
    message. Initial inline media is not supported; upload it through the agent input endpoint after launch.

        Attributes:
            content_blocks (list['TextContentBlock']):
            actor (Union[Unset, ExternalActorParams]): Identity and attributes of an external actor. Actors are upserted by
                (provider_tenant_id, provider_user_id) with the external provider. Omitted attributes keep their stored values;
                provided attributes are overwritten, including empty values. bma actors are implicit and hosted integrations own
                their own actor identities.
    """

    content_blocks: list["TextContentBlock"]
    actor: Union[Unset, "ExternalActorParams"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item = content_blocks_item_data.to_dict()
            content_blocks.append(content_blocks_item)

        actor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content_blocks": content_blocks,
            }
        )
        if actor is not UNSET:
            field_dict["actor"] = actor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.external_actor_params import ExternalActorParams
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:
            content_blocks_item = TextContentBlock.from_dict(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        _actor = d.pop("actor", UNSET)
        actor: Union[Unset, ExternalActorParams]
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = ExternalActorParams.from_dict(_actor)

        agent_launch_initial_input = cls(
            content_blocks=content_blocks,
            actor=actor,
        )

        return agent_launch_initial_input
