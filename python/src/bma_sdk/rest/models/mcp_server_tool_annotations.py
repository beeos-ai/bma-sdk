from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPServerToolAnnotations")


@_attrs_define
class MCPServerToolAnnotations:
    """
    Attributes:
        title (Union[Unset, str]):
        read_only_hint (Union[Unset, bool]):
        destructive_hint (Union[Unset, bool]):
        idempotent_hint (Union[Unset, bool]):
        open_world_hint (Union[Unset, bool]):
    """

    title: Union[Unset, str] = UNSET
    read_only_hint: Union[Unset, bool] = UNSET
    destructive_hint: Union[Unset, bool] = UNSET
    idempotent_hint: Union[Unset, bool] = UNSET
    open_world_hint: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        read_only_hint = self.read_only_hint

        destructive_hint = self.destructive_hint

        idempotent_hint = self.idempotent_hint

        open_world_hint = self.open_world_hint

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if read_only_hint is not UNSET:
            field_dict["read_only_hint"] = read_only_hint
        if destructive_hint is not UNSET:
            field_dict["destructive_hint"] = destructive_hint
        if idempotent_hint is not UNSET:
            field_dict["idempotent_hint"] = idempotent_hint
        if open_world_hint is not UNSET:
            field_dict["open_world_hint"] = open_world_hint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        read_only_hint = d.pop("read_only_hint", UNSET)

        destructive_hint = d.pop("destructive_hint", UNSET)

        idempotent_hint = d.pop("idempotent_hint", UNSET)

        open_world_hint = d.pop("open_world_hint", UNSET)

        mcp_server_tool_annotations = cls(
            title=title,
            read_only_hint=read_only_hint,
            destructive_hint=destructive_hint,
            idempotent_hint=idempotent_hint,
            open_world_hint=open_world_hint,
        )

        return mcp_server_tool_annotations
