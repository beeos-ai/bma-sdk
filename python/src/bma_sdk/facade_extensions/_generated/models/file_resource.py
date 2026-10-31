import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.file_resource_type import FileResourceType, check_file_resource_type

T = TypeVar("T", bound="FileResource")


@_attrs_define
class FileResource:
    """
    Attributes:
        id (str): Opaque, stable resource id.
        type_ (FileResourceType):
        file_id (str): The session instance created for the mount.
        mount_path (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    type_: FileResourceType
    file_id: str
    mount_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        file_id = self.file_id

        mount_path = self.mount_path

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "file_id": file_id,
                "mount_path": mount_path,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_file_resource_type(d.pop("type"))

        file_id = d.pop("file_id")

        mount_path = d.pop("mount_path")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        file_resource = cls(
            id=id,
            type_=type_,
            file_id=file_id,
            mount_path=mount_path,
            created_at=created_at,
            updated_at=updated_at,
        )

        return file_resource
