from typing import Literal, cast

ModelCatalogStatus = Literal["failed", "ok"]

MODEL_CATALOG_STATUS_VALUES: set[ModelCatalogStatus] = {
    "failed",
    "ok",
}


def check_model_catalog_status(value: str) -> ModelCatalogStatus:
    if value in MODEL_CATALOG_STATUS_VALUES:
        return cast(ModelCatalogStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_CATALOG_STATUS_VALUES!r}"
    )
