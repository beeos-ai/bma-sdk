from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine_access_source import MachineAccessSource


T = TypeVar("T", bound="MachineAccess")


@_attrs_define
class MachineAccess:
    """
    Attributes:
        can_manage (bool):
        sources (list['MachineAccessSource']):
    """

    can_manage: bool
    sources: list["MachineAccessSource"]

    def to_dict(self) -> dict[str, Any]:
        can_manage = self.can_manage

        sources = []
        for sources_item_data in self.sources:
            sources_item = sources_item_data.to_dict()
            sources.append(sources_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "can_manage": can_manage,
                "sources": sources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_access_source import MachineAccessSource

        d = dict(src_dict)
        can_manage = d.pop("can_manage")

        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = MachineAccessSource.from_dict(sources_item_data)

            sources.append(sources_item)

        machine_access = cls(
            can_manage=can_manage,
            sources=sources,
        )

        return machine_access
