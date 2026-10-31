from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.file_resource_params_type import (
    FileResourceParamsType,
    check_file_resource_params_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileResourceParams")


@_attrs_define
class FileResourceParams:
    """
    Attributes:
        type_ (FileResourceParamsType):
        file_id (str): File ID (file_...).
        mount_path (Union[None, Unset, str]): Absolute path below /mnt/session/uploads; a path outside it is placed
            under it (/data.csv mounts at /mnt/session/uploads/data.csv). Defaults to /mnt/session/uploads/<file_id>.
    """

    type_: FileResourceParamsType
    file_id: str
    mount_path: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        file_id = self.file_id

        mount_path: Union[None, Unset, str]
        if isinstance(self.mount_path, Unset):
            mount_path = UNSET
        else:
            mount_path = self.mount_path

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "file_id": file_id,
            }
        )
        if mount_path is not UNSET:
            field_dict["mount_path"] = mount_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_file_resource_params_type(d.pop("type"))

        file_id = d.pop("file_id")

        def _parse_mount_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        mount_path = _parse_mount_path(d.pop("mount_path", UNSET))

        file_resource_params = cls(
            type_=type_,
            file_id=file_id,
            mount_path=mount_path,
        )

        return file_resource_params
