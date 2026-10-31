from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageModel")


@_attrs_define
class UsageModel:
    """
    Attributes:
        configured_model_id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        provider_model_slug (str):
        model_provider_config_id (str):
        model_provider_config_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
    """

    configured_model_id: str
    name: str
    provider_model_slug: str
    model_provider_config_id: str
    model_provider_config_name: str

    def to_dict(self) -> dict[str, Any]:
        configured_model_id = self.configured_model_id

        name = self.name

        provider_model_slug = self.provider_model_slug

        model_provider_config_id = self.model_provider_config_id

        model_provider_config_name = self.model_provider_config_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "configured_model_id": configured_model_id,
                "name": name,
                "provider_model_slug": provider_model_slug,
                "model_provider_config_id": model_provider_config_id,
                "model_provider_config_name": model_provider_config_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        configured_model_id = d.pop("configured_model_id")

        name = d.pop("name")

        provider_model_slug = d.pop("provider_model_slug")

        model_provider_config_id = d.pop("model_provider_config_id")

        model_provider_config_name = d.pop("model_provider_config_name")

        usage_model = cls(
            configured_model_id=configured_model_id,
            name=name,
            provider_model_slug=provider_model_slug,
            model_provider_config_id=model_provider_config_id,
            model_provider_config_name=model_provider_config_name,
        )

        return usage_model
