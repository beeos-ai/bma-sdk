from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ListMachineBackupsResponse4XX")


@_attrs_define
class ListMachineBackupsResponse4XX:
    """
    Attributes:
        error (str): Human-readable error message. Do not match on it programmatically.
        code (str): Stable error code carried by 4XX statuses. Subset of the Error code enum whose statuses are client
            errors.
    """

    error: str
    code: str

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "code": code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code")

        list_machine_backups_response_4xx = cls(
            error=error,
            code=code,
        )

        return list_machine_backups_response_4xx
