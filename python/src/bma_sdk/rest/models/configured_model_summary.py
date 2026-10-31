import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="ConfiguredModelSummary")


@_attrs_define
class ConfiguredModelSummary:
    """
    Attributes:
        id (str):
        org_id (str):
        model_provider_config_id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        provider_config (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace
            and invisible or control characters are not.
        provider_model_slug (str): Exact provider model slug sent to the provider endpoint by the current revision.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    org_id: str
    model_provider_config_id: str
    name: str
    provider_config: str
    provider_model_slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        model_provider_config_id = self.model_provider_config_id

        name = self.name

        provider_config = self.provider_config

        provider_model_slug = self.provider_model_slug

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "model_provider_config_id": model_provider_config_id,
                "name": name,
                "provider_config": provider_config,
                "provider_model_slug": provider_model_slug,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        model_provider_config_id = d.pop("model_provider_config_id")

        name = d.pop("name")

        provider_config = d.pop("provider_config")

        provider_model_slug = d.pop("provider_model_slug")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        configured_model_summary = cls(
            id=id,
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            name=name,
            provider_config=provider_config,
            provider_model_slug=provider_model_slug,
            created_at=created_at,
            updated_at=updated_at,
        )

        return configured_model_summary
