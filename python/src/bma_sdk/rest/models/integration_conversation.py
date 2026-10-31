from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IntegrationConversation")


@_attrs_define
class IntegrationConversation:
    """One concrete provider address, validated by the integration's capabilities.subscription.conversation_schema. Slack
    uses channel_id and optional thread_ts; Discord uses channel_id for a channel or thread_id for a thread; GitHub uses
    repository_id and pull_request. Discord accepts optional parent channel_id and guild_id alongside thread_id and
    validates their ID format, but subscription creation does not verify them against Discord or retain them as routing
    restrictions. Only thread_id is retained in a canonical thread address and returned by create/list responses. No
    credentials or runtime state.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_conversation = cls()

        integration_conversation.additional_properties = d
        return integration_conversation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
