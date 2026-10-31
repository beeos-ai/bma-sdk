from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreateProjectMachineGrantRequest")


@_attrs_define
class CreateProjectMachineGrantRequest:
    """
    Attributes:
        machine_id (str): Machine ID (mch_...).
        description (Union[Unset, str]): Optional note about this grant.
        metadata (Union[Unset, Metadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters,
            values must be strings of up to 512 characters.
    """

    machine_id: str
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, "Metadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        machine_id = self.machine_id

        description = self.description

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine_id": machine_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        machine_id = d.pop("machine_id")

        description = d.pop("description", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_project_machine_grant_request = cls(
            machine_id=machine_id,
            description=description,
            metadata=metadata,
        )

        return create_project_machine_grant_request
