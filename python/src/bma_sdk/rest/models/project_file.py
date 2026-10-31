import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.project_file_type import ProjectFileType, check_project_file_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_scope import FileScope
    from ..models.project_file_metadata import ProjectFileMetadata


T = TypeVar("T", bound="ProjectFile")


@_attrs_define
class ProjectFile:
    """A project file. Field names follow the Anthropic Files API (filename, mime_type, size_bytes, scope); digest and
    metadata are BMA extensions.

        Attributes:
            id (str): File ID (file_...).
            type_ (ProjectFileType):
            org_id (str):
            project_id (str): Project ID (proj_...).
            filename (str):
            mime_type (str):
            size_bytes (int):
            digest (str): SHA-256 digest of the content, sha256:<hex>.
            metadata (ProjectFileMetadata): Caller-defined string labels.
            scope (Union['FileScope', None]): The session this file is scoped to; null for a project-wide file.
            created_at (datetime.datetime):
            source_artifact_id (Union[Unset, str]): The artifact this file was promoted from.
    """

    id: str
    type_: ProjectFileType
    org_id: str
    project_id: str
    filename: str
    mime_type: str
    size_bytes: int
    digest: str
    metadata: "ProjectFileMetadata"
    scope: Union["FileScope", None]
    created_at: datetime.datetime
    source_artifact_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_scope import FileScope

        id = self.id

        type_: str = self.type_

        org_id = self.org_id

        project_id = self.project_id

        filename = self.filename

        mime_type = self.mime_type

        size_bytes = self.size_bytes

        digest = self.digest

        metadata = self.metadata.to_dict()

        scope: Union[None, dict[str, Any]]
        if isinstance(self.scope, FileScope):
            scope = self.scope.to_dict()
        else:
            scope = self.scope

        created_at = self.created_at.isoformat()

        source_artifact_id = self.source_artifact_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "org_id": org_id,
                "project_id": project_id,
                "filename": filename,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "digest": digest,
                "metadata": metadata,
                "scope": scope,
                "created_at": created_at,
            }
        )
        if source_artifact_id is not UNSET:
            field_dict["source_artifact_id"] = source_artifact_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_scope import FileScope
        from ..models.project_file_metadata import ProjectFileMetadata

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_project_file_type(d.pop("type"))

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        filename = d.pop("filename")

        mime_type = d.pop("mime_type")

        size_bytes = d.pop("size_bytes")

        digest = d.pop("digest")

        metadata = ProjectFileMetadata.from_dict(d.pop("metadata"))

        def _parse_scope(data: object) -> Union["FileScope", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scope_type_0 = FileScope.from_dict(data)

                return scope_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FileScope", None], data)

        scope = _parse_scope(d.pop("scope"))

        created_at = isoparse(d.pop("created_at"))

        source_artifact_id = d.pop("source_artifact_id", UNSET)

        project_file = cls(
            id=id,
            type_=type_,
            org_id=org_id,
            project_id=project_id,
            filename=filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            digest=digest,
            metadata=metadata,
            scope=scope,
            created_at=created_at,
            source_artifact_id=source_artifact_id,
        )

        return project_file
