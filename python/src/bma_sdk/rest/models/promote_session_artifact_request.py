from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.promote_session_artifact_request_scope import (
    PromoteSessionArtifactRequestScope,
    check_promote_session_artifact_request_scope,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.promote_session_artifact_request_metadata import (
        PromoteSessionArtifactRequestMetadata,
    )


T = TypeVar("T", bound="PromoteSessionArtifactRequest")


@_attrs_define
class PromoteSessionArtifactRequest:
    """
    Attributes:
        filename (Union[Unset, str]): File name; defaults to the artifact's filename.
        scope (Union[Unset, PromoteSessionArtifactRequestScope]): project (default) or session (scoped to this session).
        metadata (Union[Unset, PromoteSessionArtifactRequestMetadata]): String labels for the file.
    """

    filename: Union[Unset, str] = UNSET
    scope: Union[Unset, PromoteSessionArtifactRequestScope] = UNSET
    metadata: Union[Unset, "PromoteSessionArtifactRequestMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        scope: Union[Unset, str] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if filename is not UNSET:
            field_dict["filename"] = filename
        if scope is not UNSET:
            field_dict["scope"] = scope
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.promote_session_artifact_request_metadata import (
            PromoteSessionArtifactRequestMetadata,
        )

        d = dict(src_dict)
        filename = d.pop("filename", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: Union[Unset, PromoteSessionArtifactRequestScope]
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = check_promote_session_artifact_request_scope(_scope)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, PromoteSessionArtifactRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = PromoteSessionArtifactRequestMetadata.from_dict(_metadata)

        promote_session_artifact_request = cls(
            filename=filename,
            scope=scope,
            metadata=metadata,
        )

        return promote_session_artifact_request
