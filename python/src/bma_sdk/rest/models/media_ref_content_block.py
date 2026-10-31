from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.media_ref_content_block_type import (
    MediaRefContentBlockType,
    check_media_ref_content_block_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_block_metadata import ContentBlockMetadata


T = TypeVar("T", bound="MediaRefContentBlock")


@_attrs_define
class MediaRefContentBlock:
    """
    Attributes:
        type_ (MediaRefContentBlockType):
        artifact_id (str):
        exclude_from_model_context (Union[Unset, bool]): Whether the referenced artifact is excluded from later model
            context.
        metadata (Union[Unset, ContentBlockMetadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64
            characters, values must be strings of up to 512 characters.
    """

    type_: MediaRefContentBlockType
    artifact_id: str
    exclude_from_model_context: Union[Unset, bool] = UNSET
    metadata: Union[Unset, "ContentBlockMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        artifact_id = self.artifact_id

        exclude_from_model_context = self.exclude_from_model_context

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "artifact_id": artifact_id,
            }
        )
        if exclude_from_model_context is not UNSET:
            field_dict["exclude_from_model_context"] = exclude_from_model_context
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_block_metadata import ContentBlockMetadata

        d = dict(src_dict)
        type_ = check_media_ref_content_block_type(d.pop("type"))

        artifact_id = d.pop("artifact_id")

        exclude_from_model_context = d.pop("exclude_from_model_context", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ContentBlockMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentBlockMetadata.from_dict(_metadata)

        media_ref_content_block = cls(
            type_=type_,
            artifact_id=artifact_id,
            exclude_from_model_context=exclude_from_model_context,
            metadata=metadata,
        )

        return media_ref_content_block
