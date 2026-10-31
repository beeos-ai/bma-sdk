from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.integration_settings import IntegrationSettings


T = TypeVar("T", bound="UpdateIntegrationRequest")


@_attrs_define
class UpdateIntegrationRequest:
    """Replaces integration settings. Name and integration_kind are immutable and only accepted on create. Preserve
    integration-level fields when editing launcher settings.

        Attributes:
            settings (IntegrationSettings): Integration-owned settings JSON. Validate against
                capabilities.settings.input_schema from the integration catalog. Public profile references use aprf_ IDs and
                resolve at runtime. GitHub integrations use GitHubIntegrationSettings; Slack and Discord integrations use
                ChatIntegrationSettings.
    """

    settings: "IntegrationSettings"

    def to_dict(self) -> dict[str, Any]:
        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_settings import IntegrationSettings

        d = dict(src_dict)
        settings = IntegrationSettings.from_dict(d.pop("settings"))

        update_integration_request = cls(
            settings=settings,
        )

        return update_integration_request
