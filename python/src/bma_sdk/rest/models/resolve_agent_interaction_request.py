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
    from ..models.interaction_answer import InteractionAnswer


T = TypeVar("T", bound="ResolveAgentInteractionRequest")


@_attrs_define
class ResolveAgentInteractionRequest:
    """
    Attributes:
        answers (list['InteractionAnswer']):
        actor (Union[Unset, ExternalActorParams]): Identity and attributes of an external actor. Actors are upserted by
            (provider_tenant_id, provider_user_id) with the external provider. Omitted attributes keep their stored values;
            provided attributes are overwritten, including empty values. bma actors are implicit and hosted integrations own
            their own actor identities.
    """

    answers: list["InteractionAnswer"]
    actor: Union[Unset, "ExternalActorParams"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        actor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "answers": answers,
            }
        )
        if actor is not UNSET:
            field_dict["actor"] = actor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.external_actor_params import ExternalActorParams
        from ..models.interaction_answer import InteractionAnswer

        d = dict(src_dict)
        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = InteractionAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        _actor = d.pop("actor", UNSET)
        actor: Union[Unset, ExternalActorParams]
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = ExternalActorParams.from_dict(_actor)

        resolve_agent_interaction_request = cls(
            answers=answers,
            actor=actor,
        )

        return resolve_agent_interaction_request
