from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.event_webhook_event_type import (
    EventWebhookEventType,
    check_event_webhook_event_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateEventWebhookRequest")


@_attrs_define
class UpdateEventWebhookRequest:
    """
    Attributes:
        url (Union[Unset, str]): Public HTTPS endpoint, at most 2048 bytes after URL encoding.
        event_types (Union[Unset, list[EventWebhookEventType]]):
        signing_secret_id (Union[None, Unset, str]): Project-available generic secret. Omit to preserve signing, or set
            to null to remove it.
    """

    url: Union[Unset, str] = UNSET
    event_types: Union[Unset, list[EventWebhookEventType]] = UNSET
    signing_secret_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        event_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = []
            for event_types_item_data in self.event_types:
                event_types_item: str = event_types_item_data
                event_types.append(event_types_item)

        signing_secret_id: Union[None, Unset, str]
        if isinstance(self.signing_secret_id, Unset):
            signing_secret_id = UNSET
        else:
            signing_secret_id = self.signing_secret_id

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if event_types is not UNSET:
            field_dict["event_types"] = event_types
        if signing_secret_id is not UNSET:
            field_dict["signing_secret_id"] = signing_secret_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        event_types = []
        _event_types = d.pop("event_types", UNSET)
        for event_types_item_data in _event_types or []:
            event_types_item = check_event_webhook_event_type(event_types_item_data)

            event_types.append(event_types_item)

        def _parse_signing_secret_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        signing_secret_id = _parse_signing_secret_id(d.pop("signing_secret_id", UNSET))

        update_event_webhook_request = cls(
            url=url,
            event_types=event_types,
            signing_secret_id=signing_secret_id,
        )

        return update_event_webhook_request
