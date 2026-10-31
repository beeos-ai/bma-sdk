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
    from ..models.artifact import Artifact


T = TypeVar("T", bound="SessionArtifactList")


@_attrs_define
class SessionArtifactList:
    """
    Attributes:
        data (list['Artifact']):
        next_cursor (Union[None, str]):
    """

    data: list["Artifact"]
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
        from ..models.artifact import Artifact

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Artifact.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        session_artifact_list = cls(
            data=data,
            next_cursor=next_cursor,
        )

        return session_artifact_list
