from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.event_webhook import EventWebhook


T = TypeVar("T", bound="ListEventWebhooksResponse")


@_attrs_define
class ListEventWebhooksResponse:
    """
    Attributes:
        data (list['EventWebhook']):
    """

    data: list["EventWebhook"]

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
        from ..models.event_webhook import EventWebhook

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = EventWebhook.from_dict(data_item_data)

            data.append(data_item)

        list_event_webhooks_response = cls(
            data=data,
        )

        return list_event_webhooks_response
