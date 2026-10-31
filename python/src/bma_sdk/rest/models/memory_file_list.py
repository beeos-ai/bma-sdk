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
    from ..models.memory_directory import MemoryDirectory
    from ..models.memory_regular_file import MemoryRegularFile


T = TypeVar("T", bound="MemoryFileList")


@_attrs_define
class MemoryFileList:
    """
    Attributes:
        data (list[Union['MemoryDirectory', 'MemoryRegularFile']]):
        next_cursor (Union[None, str]):
    """

    data: list[Union["MemoryDirectory", "MemoryRegularFile"]]
    next_cursor: Union[None, str]

    def to_dict(self) -> dict[str, Any]:
        from ..models.memory_regular_file import MemoryRegularFile

        data = []
        for data_item_data in self.data:
            data_item: dict[str, Any]
            if isinstance(data_item_data, MemoryRegularFile):
                data_item = data_item_data.to_dict()
            else:
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
        from ..models.memory_directory import MemoryDirectory
        from ..models.memory_regular_file import MemoryRegularFile

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:

            def _parse_data_item(
                data: object,
            ) -> Union["MemoryDirectory", "MemoryRegularFile"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_memory_file_type_0 = MemoryRegularFile.from_dict(
                        data
                    )

                    return componentsschemas_memory_file_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_memory_file_type_1 = MemoryDirectory.from_dict(data)

                return componentsschemas_memory_file_type_1

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        memory_file_list = cls(
            data=data,
            next_cursor=next_cursor,
        )

        return memory_file_list
