from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.text_content_block_type import (
    TextContentBlockType,
    check_text_content_block_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_block_metadata import ContentBlockMetadata


T = TypeVar("T", bound="TextContentBlock")


@_attrs_define
class TextContentBlock:
    """
    Attributes:
        type_ (TextContentBlockType):
        text (str):
        metadata (Union[Unset, ContentBlockMetadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64
            characters, values must be strings of up to 512 characters.
    """

    type_: TextContentBlockType
    text: str
    metadata: Union[Unset, "ContentBlockMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        text = self.text

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "text": text,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_block_metadata import ContentBlockMetadata

        d = dict(src_dict)
        type_ = check_text_content_block_type(d.pop("type"))

        text = d.pop("text")

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ContentBlockMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentBlockMetadata.from_dict(_metadata)

        text_content_block = cls(
            type_=type_,
            text=text,
            metadata=metadata,
        )

        return text_content_block
