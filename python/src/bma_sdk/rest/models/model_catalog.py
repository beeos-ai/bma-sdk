from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_catalog_status import ModelCatalogStatus, check_model_catalog_status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.discovered_provider_model import DiscoveredProviderModel


T = TypeVar("T", bound="ModelCatalog")


@_attrs_define
class ModelCatalog:
    """The provider's model catalog, obtained by validating the configured credential and probing the provider's /models
    endpoint. A failed probe does not affect the stored config; treat it as a warning that the base URL or API key may
    be invalid.

        Attributes:
            status (ModelCatalogStatus):
            models (Union[Unset, list['DiscoveredProviderModel']]): Models advertised by the provider, newest first,
                filtered to text-output tool-calling models where the provider exposes enough metadata to tell. Present when
                status is ok.
            error (Union[Unset, str]): Why the probe failed. Present when status is failed.
    """

    status: ModelCatalogStatus
    models: Union[Unset, list["DiscoveredProviderModel"]] = UNSET
    error: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        models: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()
                models.append(models_item)

        error = self.error

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
            }
        )
        if models is not UNSET:
            field_dict["models"] = models
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discovered_provider_model import DiscoveredProviderModel

        d = dict(src_dict)
        status = check_model_catalog_status(d.pop("status"))

        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = DiscoveredProviderModel.from_dict(models_item_data)

            models.append(models_item)

        error = d.pop("error", UNSET)

        model_catalog = cls(
            status=status,
            models=models,
            error=error,
        )

        return model_catalog
