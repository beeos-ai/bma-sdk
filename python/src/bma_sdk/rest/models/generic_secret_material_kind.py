from typing import Literal, cast

GenericSecretMaterialKind = Literal["generic"]

GENERIC_SECRET_MATERIAL_KIND_VALUES: set[GenericSecretMaterialKind] = {
    "generic",
}


def check_generic_secret_material_kind(value: str) -> GenericSecretMaterialKind:
    if value in GENERIC_SECRET_MATERIAL_KIND_VALUES:
        return cast(GenericSecretMaterialKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GENERIC_SECRET_MATERIAL_KIND_VALUES!r}"
    )
