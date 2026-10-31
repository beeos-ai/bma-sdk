from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.integration_kind import IntegrationKind, check_integration_kind

if TYPE_CHECKING:
    from ..models.integration_capabilities import IntegrationCapabilities


T = TypeVar("T", bound="IntegrationDefinition")


@_attrs_define
class IntegrationDefinition:
    """
    Attributes:
        integration_kind (IntegrationKind): Registered integration implementation; independent of the saved
            integration's name and immutable ID.
        capabilities (IntegrationCapabilities):
    """

    integration_kind: IntegrationKind
    capabilities: "IntegrationCapabilities"

    def to_dict(self) -> dict[str, Any]:
        integration_kind: str = self.integration_kind

        capabilities = self.capabilities.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration_kind": integration_kind,
                "capabilities": capabilities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_capabilities import IntegrationCapabilities

        d = dict(src_dict)
        integration_kind = check_integration_kind(d.pop("integration_kind"))

        capabilities = IntegrationCapabilities.from_dict(d.pop("capabilities"))

        integration_definition = cls(
            integration_kind=integration_kind,
            capabilities=capabilities,
        )

        return integration_definition
