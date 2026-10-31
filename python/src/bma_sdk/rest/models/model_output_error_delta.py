from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_error_delta_kind import (
    ModelOutputErrorDeltaKind,
    check_model_output_error_delta_kind,
)

if TYPE_CHECKING:
    from ..models.model_output_error_delta_error import ModelOutputErrorDeltaError


T = TypeVar("T", bound="ModelOutputErrorDelta")


@_attrs_define
class ModelOutputErrorDelta:
    """
    Attributes:
        kind (ModelOutputErrorDeltaKind):
        error (ModelOutputErrorDeltaError):
    """

    kind: ModelOutputErrorDeltaKind
    error: "ModelOutputErrorDeltaError"

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_output_error_delta_error import ModelOutputErrorDeltaError

        d = dict(src_dict)
        kind = check_model_output_error_delta_kind(d.pop("kind"))

        error = ModelOutputErrorDeltaError.from_dict(d.pop("error"))

        model_output_error_delta = cls(
            kind=kind,
            error=error,
        )

        return model_output_error_delta
