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
    from ..models.agent_session import AgentSession


T = TypeVar("T", bound="ListProjectAgentSessionsResponse")


@_attrs_define
class ListProjectAgentSessionsResponse:
    """
    Attributes:
        data (list['AgentSession']):
        next_after_id (Union[None, str]): The `after_id` of the next page, or null on the last page.
    """

    data: list["AgentSession"]
    next_after_id: Union[None, str]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_after_id: Union[None, str]
        next_after_id = self.next_after_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_after_id": next_after_id,
            }
        )

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

        def _parse_next_after_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_after_id = _parse_next_after_id(d.pop("next_after_id"))

        list_project_agent_sessions_response = cls(
            data=data,
            next_after_id=next_after_id,
        )

        return list_project_agent_sessions_response
