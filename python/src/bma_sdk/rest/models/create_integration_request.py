from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.integration_kind import IntegrationKind, check_integration_kind

if TYPE_CHECKING:
    from ..models.integration_settings import IntegrationSettings


T = TypeVar("T", bound="CreateIntegrationRequest")


@_attrs_define
class CreateIntegrationRequest:
    """Creates a disconnected integration. Name and integration_kind are immutable. Configure credentials through this
    integration's setup endpoints.

        Attributes:
            name (str): Immutable, project-unique integration name used in config keys and qualified tool names.
            integration_kind (IntegrationKind): Registered integration implementation; independent of the saved
                integration's name and immutable ID.
            settings (IntegrationSettings): Integration-owned settings JSON. Validate against
                capabilities.settings.input_schema from the integration catalog. Public profile references use aprf_ IDs and
                resolve at runtime. GitHub integrations use GitHubIntegrationSettings; Slack and Discord integrations use
                ChatIntegrationSettings.
    """

    name: str
    integration_kind: IntegrationKind
    settings: "IntegrationSettings"

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        integration_kind: str = self.integration_kind

        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "integration_kind": integration_kind,
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_settings import IntegrationSettings

        d = dict(src_dict)
        name = d.pop("name")

        integration_kind = check_integration_kind(d.pop("integration_kind"))

        settings = IntegrationSettings.from_dict(d.pop("settings"))

        create_integration_request = cls(
            name=name,
            integration_kind=integration_kind,
            settings=settings,
        )

        return create_integration_request
