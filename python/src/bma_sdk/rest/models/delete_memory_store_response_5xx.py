from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DeleteMemoryStoreResponse5XX")


@_attrs_define
class DeleteMemoryStoreResponse5XX:
    """
    Attributes:
        error (str): Human-readable error message. Do not match on it programmatically.
        code (str): Stable error code carried by 5XX statuses. Subset of the Error code enum whose statuses are server
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

        delete_memory_store_response_5xx = cls(
            error=error,
            code=code,
        )

        return delete_memory_store_response_5xx
