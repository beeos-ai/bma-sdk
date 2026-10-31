from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTerminalSessionRequest")


@_attrs_define
class CreateTerminalSessionRequest:
    """
    Attributes:
        shell (Union[Unset, str]):
        cwd (Union[Unset, str]):
        cols (Union[Unset, int]):
        rows (Union[Unset, int]):
    """

    shell: Union[Unset, str] = UNSET
    cwd: Union[Unset, str] = UNSET
    cols: Union[Unset, int] = UNSET
    rows: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        shell = self.shell

        cwd = self.cwd

        cols = self.cols

        rows = self.rows

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if shell is not UNSET:
            field_dict["shell"] = shell
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if cols is not UNSET:
            field_dict["cols"] = cols
        if rows is not UNSET:
            field_dict["rows"] = rows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        shell = d.pop("shell", UNSET)

        cwd = d.pop("cwd", UNSET)

        cols = d.pop("cols", UNSET)

        rows = d.pop("rows", UNSET)

        create_terminal_session_request = cls(
            shell=shell,
            cwd=cwd,
            cols=cols,
            rows=rows,
        )

        return create_terminal_session_request
