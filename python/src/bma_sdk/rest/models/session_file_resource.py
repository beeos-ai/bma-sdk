import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.session_file_resource_type import (
    SessionFileResourceType,
    check_session_file_resource_type,
)

T = TypeVar("T", bound="SessionFileResource")


@_attrs_define
class SessionFileResource:
    """A file mounted into a session. file_id is the session instance created for the mount, not the mounted file's id; GET
    /files/{file_id} and its content read it.

        Attributes:
            id (str):
            type_ (SessionFileResourceType):
            file_id (str): File ID (file_...).
            mount_path (str): Absolute path the session's tools read the file at.
            filename (str):
            mime_type (str):
            size_bytes (int):
            digest (str):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
    """

    id: str
    type_: SessionFileResourceType
    file_id: str
    mount_path: str
    filename: str
    mime_type: str
    size_bytes: int
    digest: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        file_id = self.file_id

        mount_path = self.mount_path

        filename = self.filename

        mime_type = self.mime_type

        size_bytes = self.size_bytes

        digest = self.digest

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "file_id": file_id,
                "mount_path": mount_path,
                "filename": filename,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "digest": digest,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_session_file_resource_type(d.pop("type"))

        file_id = d.pop("file_id")

        mount_path = d.pop("mount_path")

        filename = d.pop("filename")

        mime_type = d.pop("mime_type")

        size_bytes = d.pop("size_bytes")

        digest = d.pop("digest")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        session_file_resource = cls(
            id=id,
            type_=type_,
            file_id=file_id,
            mount_path=mount_path,
            filename=filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            digest=digest,
            created_at=created_at,
            updated_at=updated_at,
        )

        return session_file_resource
