from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.daemon_session_file import DaemonSessionFile


T = TypeVar("T", bound="DaemonSessionFiles")


@_attrs_define
class DaemonSessionFiles:
    """The files mounted into an agent session.

    Attributes:
        session_id (str):
        files (list['DaemonSessionFile']):
    """

    session_id: str
    files: list["DaemonSessionFile"]

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "session_id": session_id,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daemon_session_file import DaemonSessionFile

        d = dict(src_dict)
        session_id = d.pop("session_id")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = DaemonSessionFile.from_dict(files_item_data)

            files.append(files_item)

        daemon_session_files = cls(
            session_id=session_id,
            files=files,
        )

        return daemon_session_files
