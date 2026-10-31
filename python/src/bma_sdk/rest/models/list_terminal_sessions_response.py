from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.terminal_session import TerminalSession


T = TypeVar("T", bound="ListTerminalSessionsResponse")


@_attrs_define
class ListTerminalSessionsResponse:
    """
    Attributes:
        data (list['TerminalSession']):
    """

    data: list["TerminalSession"]

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
        from ..models.terminal_session import TerminalSession

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TerminalSession.from_dict(data_item_data)

            data.append(data_item)

        list_terminal_sessions_response = cls(
            data=data,
        )

        return list_terminal_sessions_response
