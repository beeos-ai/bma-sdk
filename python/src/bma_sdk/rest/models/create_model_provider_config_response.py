from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.model_catalog import ModelCatalog
    from ..models.model_provider_config import ModelProviderConfig


T = TypeVar("T", bound="CreateModelProviderConfigResponse")


@_attrs_define
class CreateModelProviderConfigResponse:
    """
    Attributes:
        config (ModelProviderConfig):
        model_catalog (ModelCatalog): The provider's model catalog, obtained by validating the configured credential and
            probing the provider's /models endpoint. A failed probe does not affect the stored config; treat it as a warning
            that the base URL or API key may be invalid.
    """

    config: "ModelProviderConfig"
    model_catalog: "ModelCatalog"

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        model_catalog = self.model_catalog.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "config": config,
                "model_catalog": model_catalog,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_catalog import ModelCatalog
        from ..models.model_provider_config import ModelProviderConfig

        d = dict(src_dict)
        config = ModelProviderConfig.from_dict(d.pop("config"))

        model_catalog = ModelCatalog.from_dict(d.pop("model_catalog"))

        create_model_provider_config_response = cls(
            config=config,
            model_catalog=model_catalog,
        )

        return create_model_provider_config_response
