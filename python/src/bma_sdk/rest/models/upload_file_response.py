from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UploadFileResponse")


@_attrs_define
class UploadFileResponse:
    """Returns the uploaded file's path and digest.

    Attributes:
        path (str):
        digest (str):
    """

    path: str
    digest: str

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        digest = self.digest

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "digest": digest,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        digest = d.pop("digest")

        upload_file_response = cls(
            path=path,
            digest=digest,
        )

        return upload_file_response
