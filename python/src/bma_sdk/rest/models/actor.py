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

from ..models.actor_provider import ActorProvider, check_actor_provider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Actor")


@_attrs_define
class Actor:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        provider (ActorProvider): bma for BMA identities, integration for hosted integration senders, or external for
            API-managed actors.
        provider_user_id (str): Stable sender identifier within the actor identity namespace.
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        provider_tenant_id (Union[Unset, str]): Project-scoped identity namespace. Integration actors use a stable
            platform namespace (slack:<workspace ID>, discord, or github:github.com), shared across configured bots and
            integration kinds on that platform. Retained for attribution after integration deletion; not an authorization
            principal.
        display_name (Union[Unset, str]):
    """

    id: str
    org_id: str
    project_id: str
    provider: ActorProvider
    provider_user_id: str
    metadata: "Metadata"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provider_tenant_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        provider: str = self.provider

        provider_user_id = self.provider_user_id

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provider_tenant_id = self.provider_tenant_id

        display_name = self.display_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "provider": provider,
                "provider_user_id": provider_user_id,
                "metadata": metadata,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if provider_tenant_id is not UNSET:
            field_dict["provider_tenant_id"] = provider_tenant_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        provider = check_actor_provider(d.pop("provider"))

        provider_user_id = d.pop("provider_user_id")

        metadata = Metadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        provider_tenant_id = d.pop("provider_tenant_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        actor = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            provider=provider,
            provider_user_id=provider_user_id,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            provider_tenant_id=provider_tenant_id,
            display_name=display_name,
        )

        return actor
