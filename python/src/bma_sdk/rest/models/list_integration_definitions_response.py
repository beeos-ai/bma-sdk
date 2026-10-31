from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.integration_definition import IntegrationDefinition


T = TypeVar("T", bound="ListIntegrationDefinitionsResponse")


@_attrs_define
class ListIntegrationDefinitionsResponse:
    """
    Attributes:
        data (list['IntegrationDefinition']):
    """

    data: list["IntegrationDefinition"]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_definition import IntegrationDefinition

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = IntegrationDefinition.from_dict(data_item_data)

            data.append(data_item)

        list_integration_definitions_response = cls(
            data=data,
        )

        return list_integration_definitions_response
