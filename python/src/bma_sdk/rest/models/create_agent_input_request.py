from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.create_agent_input_delivery_mode import (
    CreateAgentInputDeliveryMode,
    check_create_agent_input_delivery_mode,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_model_override_input import AgentModelOverrideInput
    from ..models.external_actor_params import ExternalActorParams
    from ..models.inline_media_content_block import InlineMediaContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="CreateAgentInputRequest")


@_attrs_define
class CreateAgentInputRequest:
    """
    Attributes:
        content_blocks (list[Union['InlineMediaContentBlock', 'TextContentBlock']]): At most 20 inline media blocks per
            submission, each holding up to 10 MiB of decoded media and up to 24 MiB decoded across the submission. Non-media
            blocks may hold up to 1 MiB combined. The whole request body is capped at 48 MiB.
        delivery_mode (Union[Unset, CreateAgentInputDeliveryMode]):
        cancel_open_interactions (Union[Unset, bool]): Only valid when delivery_mode is steering. When true, atomically
            cancels open interactions associated with the current turn's unfinished tool calls before creating the steering
            input. Their parent tool calls complete as canceled; the turn, runtime, and unrelated tool calls are preserved.
        actor (Union[Unset, ExternalActorParams]): Identity and attributes of an external actor. Actors are upserted by
            (provider_tenant_id, provider_user_id) with the external provider. Omitted attributes keep their stored values;
            provided attributes are overwritten, including empty values. bma actors are implicit and hosted integrations own
            their own actor identities.
        model_override (Union[Unset, AgentModelOverrideInput]):
    """

    content_blocks: list[Union["InlineMediaContentBlock", "TextContentBlock"]]
    delivery_mode: Union[Unset, CreateAgentInputDeliveryMode] = UNSET
    cancel_open_interactions: Union[Unset, bool] = UNSET
    actor: Union[Unset, "ExternalActorParams"] = UNSET
    model_override: Union[Unset, "AgentModelOverrideInput"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_content_block import TextContentBlock

        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item: dict[str, Any]
            if isinstance(content_blocks_item_data, TextContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            else:
                content_blocks_item = content_blocks_item_data.to_dict()

            content_blocks.append(content_blocks_item)

        delivery_mode: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_mode, Unset):
            delivery_mode = self.delivery_mode

        cancel_open_interactions = self.cancel_open_interactions

        actor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        model_override: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model_override, Unset):
            model_override = self.model_override.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content_blocks": content_blocks,
            }
        )
        if delivery_mode is not UNSET:
            field_dict["delivery_mode"] = delivery_mode
        if cancel_open_interactions is not UNSET:
            field_dict["cancel_open_interactions"] = cancel_open_interactions
        if actor is not UNSET:
            field_dict["actor"] = actor
        if model_override is not UNSET:
            field_dict["model_override"] = model_override

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_model_override_input import AgentModelOverrideInput
        from ..models.external_actor_params import ExternalActorParams
        from ..models.inline_media_content_block import InlineMediaContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:

            def _parse_content_blocks_item(
                data: object,
            ) -> Union["InlineMediaContentBlock", "TextContentBlock"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_create_agent_input_content_block_type_0 = (
                        TextContentBlock.from_dict(data)
                    )

                    return componentsschemas_create_agent_input_content_block_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_create_agent_input_content_block_type_1 = (
                    InlineMediaContentBlock.from_dict(data)
                )

                return componentsschemas_create_agent_input_content_block_type_1

            content_blocks_item = _parse_content_blocks_item(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        _delivery_mode = d.pop("delivery_mode", UNSET)
        delivery_mode: Union[Unset, CreateAgentInputDeliveryMode]
        if isinstance(_delivery_mode, Unset):
            delivery_mode = UNSET
        else:
            delivery_mode = check_create_agent_input_delivery_mode(_delivery_mode)

        cancel_open_interactions = d.pop("cancel_open_interactions", UNSET)

        _actor = d.pop("actor", UNSET)
        actor: Union[Unset, ExternalActorParams]
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = ExternalActorParams.from_dict(_actor)

        _model_override = d.pop("model_override", UNSET)
        model_override: Union[Unset, AgentModelOverrideInput]
        if isinstance(_model_override, Unset):
            model_override = UNSET
        else:
            model_override = AgentModelOverrideInput.from_dict(_model_override)

        create_agent_input_request = cls(
            content_blocks=content_blocks,
            delivery_mode=delivery_mode,
            cancel_open_interactions=cancel_open_interactions,
            actor=actor,
            model_override=model_override,
        )

        return create_agent_input_request
