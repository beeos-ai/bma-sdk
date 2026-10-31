from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CompiledIntegrationCapability")


@_attrs_define
class CompiledIntegrationCapability:
    """
    Attributes:
        integration_id (str):
    """

    integration_id: str

    def to_dict(self) -> dict[str, Any]:
        integration_id = self.integration_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration_id": integration_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_id = d.pop("integration_id")

        compiled_integration_capability = cls(
            integration_id=integration_id,
        )

        return compiled_integration_capability
