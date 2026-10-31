import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.terminal_session_state import (
    TerminalSessionState,
    check_terminal_session_state,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalSession")


@_attrs_define
class TerminalSession:
    """
    Attributes:
        id (str): Terminal session ID (tsn_...).
        org_id (str):
        project_id (str): Project ID (proj_...).
        machine_id (str): Machine ID (mch_...).
        state (TerminalSessionState):
        created_at (datetime.datetime):
        shell (Union[Unset, str]):
        cwd (Union[Unset, str]):
        cols (Union[Unset, int]):
        rows (Union[Unset, int]):
        closed_at (Union[Unset, datetime.datetime]):
        exit_code (Union[Unset, int]):
        close_reason (Union[Unset, str]):
    """

    id: str
    org_id: str
    project_id: str
    machine_id: str
    state: TerminalSessionState
    created_at: datetime.datetime
    shell: Union[Unset, str] = UNSET
    cwd: Union[Unset, str] = UNSET
    cols: Union[Unset, int] = UNSET
    rows: Union[Unset, int] = UNSET
    closed_at: Union[Unset, datetime.datetime] = UNSET
    exit_code: Union[Unset, int] = UNSET
    close_reason: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        machine_id = self.machine_id

        state: str = self.state

        created_at = self.created_at.isoformat()

        shell = self.shell

        cwd = self.cwd

        cols = self.cols

        rows = self.rows

        closed_at: Union[Unset, str] = UNSET
        if not isinstance(self.closed_at, Unset):
            closed_at = self.closed_at.isoformat()

        exit_code = self.exit_code

        close_reason = self.close_reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "machine_id": machine_id,
                "state": state,
                "created_at": created_at,
            }
        )
        if shell is not UNSET:
            field_dict["shell"] = shell
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if cols is not UNSET:
            field_dict["cols"] = cols
        if rows is not UNSET:
            field_dict["rows"] = rows
        if closed_at is not UNSET:
            field_dict["closed_at"] = closed_at
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if close_reason is not UNSET:
            field_dict["close_reason"] = close_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        machine_id = d.pop("machine_id")

        state = check_terminal_session_state(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        shell = d.pop("shell", UNSET)

        cwd = d.pop("cwd", UNSET)

        cols = d.pop("cols", UNSET)

        rows = d.pop("rows", UNSET)

        _closed_at = d.pop("closed_at", UNSET)
        closed_at: Union[Unset, datetime.datetime]
        if isinstance(_closed_at, Unset):
            closed_at = UNSET
        else:
            closed_at = isoparse(_closed_at)

        exit_code = d.pop("exit_code", UNSET)

        close_reason = d.pop("close_reason", UNSET)

        terminal_session = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            state=state,
            created_at=created_at,
            shell=shell,
            cwd=cwd,
            cols=cols,
            rows=rows,
            closed_at=closed_at,
            exit_code=exit_code,
            close_reason=close_reason,
        )

        return terminal_session
