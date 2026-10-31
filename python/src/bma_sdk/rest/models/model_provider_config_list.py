from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.model_provider_config import ModelProviderConfig


T = TypeVar("T", bound="ModelProviderConfigList")


@_attrs_define
class ModelProviderConfigList:
    """
    Attributes:
        data (list['ModelProviderConfig']):
        next_cursor (Union[None, str]):
    """

    data: list["ModelProviderConfig"]
    next_cursor: Union[None, str]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_cursor: Union[None, str]
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_provider_config import ModelProviderConfig

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ModelProviderConfig.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        model_provider_config_list = cls(
            data=data,
            next_cursor=next_cursor,
        )

        return model_provider_config_list
