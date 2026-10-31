from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.generic_secret_material_kind import (
    GenericSecretMaterialKind,
    check_generic_secret_material_kind,
)

T = TypeVar("T", bound="GenericSecretMaterial")


@_attrs_define
class GenericSecretMaterial:
    """
    Attributes:
        kind (GenericSecretMaterialKind):
        value (str):
    """

    kind: GenericSecretMaterialKind
    value: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_generic_secret_material_kind(d.pop("kind"))

        value = d.pop("value")

        generic_secret_material = cls(
            kind=kind,
            value=value,
        )

        return generic_secret_material
