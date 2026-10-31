from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.inline_media_content_block_media_type import (
    InlineMediaContentBlockMediaType,
    check_inline_media_content_block_media_type,
)
from ..models.inline_media_content_block_type import (
    InlineMediaContentBlockType,
    check_inline_media_content_block_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_block_metadata import ContentBlockMetadata


T = TypeVar("T", bound="InlineMediaContentBlock")


@_attrs_define
class InlineMediaContentBlock:
    """Files that pass validation are stored as artifacts. Model input always includes the artifact ID, whether or not the
    file contents can be sent directly. Text media must contain valid UTF-8 and is sent as text. Images and PDFs are
    sent directly when supported by the configured provider and model; unsupported combinations are rejected. Other
    binary documents are sent directly only to OpenAI Responses models with file input support. Chat Completions and
    Anthropic Messages receive the artifact ID and the filename, if provided, instead of the contents of those
    documents.

        Attributes:
            type_ (InlineMediaContentBlockType):
            media_type (InlineMediaContentBlockMediaType):
            data (str): Base64-encoded file bytes. For text media types, the decoded bytes must be valid UTF-8.
            filename (Union[Unset, str]):
            metadata (Union[Unset, ContentBlockMetadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64
                characters, values must be strings of up to 512 characters.
    """

    type_: InlineMediaContentBlockType
    media_type: InlineMediaContentBlockMediaType
    data: str
    filename: Union[Unset, str] = UNSET
    metadata: Union[Unset, "ContentBlockMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        media_type: str = self.media_type

        data = self.data

        filename = self.filename

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "media_type": media_type,
                "data": data,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_block_metadata import ContentBlockMetadata

        d = dict(src_dict)
        type_ = check_inline_media_content_block_type(d.pop("type"))

        media_type = check_inline_media_content_block_media_type(d.pop("media_type"))

        data = d.pop("data")

        filename = d.pop("filename", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ContentBlockMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentBlockMetadata.from_dict(_metadata)

        inline_media_content_block = cls(
            type_=type_,
            media_type=media_type,
            data=data,
            filename=filename,
            metadata=metadata,
        )

        return inline_media_content_block
