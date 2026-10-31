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
    from ..models.session_file import SessionFile


T = TypeVar("T", bound="SessionFilePage")


@_attrs_define
class SessionFilePage:
    """
    Attributes:
        data (list['SessionFile']):
        next_page (Union[None, str]):
    """

    data: list["SessionFile"]
    next_page: Union[None, str]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_page: Union[None, str]
        next_page = self.next_page

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_page": next_page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_file import SessionFile

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = SessionFile.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_page(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_page = _parse_next_page(d.pop("next_page"))

        session_file_page = cls(
            data=data,
            next_page=next_page,
        )

        return session_file_page
