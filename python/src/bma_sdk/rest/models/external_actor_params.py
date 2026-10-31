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
    from ..models.metadata import Metadata


T = TypeVar("T", bound="ExternalActorParams")


@_attrs_define
class ExternalActorParams:
    """Identity and attributes of an external actor. Actors are upserted by (provider_tenant_id, provider_user_id) with the
    external provider. Omitted attributes keep their stored values; provided attributes are overwritten, including empty
    values. bma actors are implicit and hosted integrations own their own actor identities.

        Attributes:
            provider_user_id (str):
            provider_tenant_id (Union[Unset, str]):
            display_name (Union[Unset, str]):
            metadata (Union[Unset, Metadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters,
                values must be strings of up to 512 characters.
    """

    provider_user_id: str
    provider_tenant_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    metadata: Union[Unset, "Metadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider_user_id = self.provider_user_id

        provider_tenant_id = self.provider_tenant_id

        display_name = self.display_name

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_user_id": provider_user_id,
            }
        )
        if provider_tenant_id is not UNSET:
            field_dict["provider_tenant_id"] = provider_tenant_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        provider_user_id = d.pop("provider_user_id")

        provider_tenant_id = d.pop("provider_tenant_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        external_actor_params = cls(
            provider_user_id=provider_user_id,
            provider_tenant_id=provider_tenant_id,
            display_name=display_name,
            metadata=metadata,
        )

        return external_actor_params
