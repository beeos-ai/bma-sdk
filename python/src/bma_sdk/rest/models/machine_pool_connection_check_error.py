from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.machine_pool_connection_check_error_code import (
    MachinePoolConnectionCheckErrorCode,
    check_machine_pool_connection_check_error_code,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MachinePoolConnectionCheckError")


@_attrs_define
class MachinePoolConnectionCheckError:
    """
    Attributes:
        error (str): Why the check failed, in plain language. Do not match on it programmatically.
        code (MachinePoolConnectionCheckErrorCode):
        details (Union[Unset, str]): The provider's original error, for troubleshooting. Present when the provider call
            failed.
    """

    error: str
    code: MachinePoolConnectionCheckErrorCode
    details: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code: str = self.code

        details = self.details

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "code": code,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = check_machine_pool_connection_check_error_code(d.pop("code"))

        details = d.pop("details", UNSET)

        machine_pool_connection_check_error = cls(
            error=error,
            code=code,
            details=details,
        )

        return machine_pool_connection_check_error
