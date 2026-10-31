from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RestoreMachineFromBackupRequest")


@_attrs_define
class RestoreMachineFromBackupRequest:
    """
    Attributes:
        backup_id (Union[Unset, str]): The ready backup to restore; defaults to the newest.
    """

    backup_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if backup_id is not UNSET:
            field_dict["backup_id"] = backup_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backup_id = d.pop("backup_id", UNSET)

        restore_machine_from_backup_request = cls(
            backup_id=backup_id,
        )

        return restore_machine_from_backup_request
