from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_session import AgentSession


T = TypeVar("T", bound="ListAgentSessionsResponse")


@_attrs_define
class ListAgentSessionsResponse:
    """
    Attributes:
        data (list['AgentSession']):
        next_before_id (Union[None, Unset, str]):
    """

    data: list["AgentSession"]
    next_before_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_before_id: Union[None, Unset, str]
        if isinstance(self.next_before_id, Unset):
            next_before_id = UNSET
        else:
            next_before_id = self.next_before_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )
        if next_before_id is not UNSET:
            field_dict["next_before_id"] = next_before_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_session import AgentSession

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AgentSession.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_before_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        next_before_id = _parse_next_before_id(d.pop("next_before_id", UNSET))

        list_agent_sessions_response = cls(
            data=data,
            next_before_id=next_before_id,
        )

        return list_agent_sessions_response
