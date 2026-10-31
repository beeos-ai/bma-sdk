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


T = TypeVar("T", bound="CancelAgentRequest")


@_attrs_define
class CancelAgentRequest:
    """
    Attributes:
        actor (Union[Unset, ExternalActorParams]): Identity and attributes of an external actor. Actors are upserted by
            (provider_tenant_id, provider_user_id) with the external provider. Omitted attributes keep their stored values;
            provided attributes are overwritten, including empty values. bma actors are implicit and hosted integrations own
            their own actor identities.
    """

    actor: Union[Unset, "ExternalActorParams"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        actor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if actor is not UNSET:
            field_dict["actor"] = actor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.external_actor_params import ExternalActorParams

        d = dict(src_dict)
        _actor = d.pop("actor", UNSET)
        actor: Union[Unset, ExternalActorParams]
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = ExternalActorParams.from_dict(_actor)

        cancel_agent_request = cls(
            actor=actor,
        )

        return cancel_agent_request
