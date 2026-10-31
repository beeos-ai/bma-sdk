from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.integration_cron_trigger_target_type import (
    IntegrationCronTriggerTargetType,
    check_integration_cron_trigger_target_type,
)

if TYPE_CHECKING:
    from ..models.integration_cron_trigger_target_settings import (
        IntegrationCronTriggerTargetSettings,
    )


T = TypeVar("T", bound="IntegrationCronTriggerTarget")


@_attrs_define
class IntegrationCronTriggerTarget:
    """
    Attributes:
        type_ (IntegrationCronTriggerTargetType):
        integration_id (str):
        settings (IntegrationCronTriggerTargetSettings): Settings validated by the target integration's published
            schedule input schema. Each accepted occurrence retains its own copy. Integration resource references are
            resolved when the integration handles the occurrence.
    """

    type_: IntegrationCronTriggerTargetType
    integration_id: str
    settings: "IntegrationCronTriggerTargetSettings"

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        integration_id = self.integration_id

        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "integration_id": integration_id,
                "settings": settings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_cron_trigger_target_settings import (
            IntegrationCronTriggerTargetSettings,
        )

        d = dict(src_dict)
        type_ = check_integration_cron_trigger_target_type(d.pop("type"))

        integration_id = d.pop("integration_id")

        settings = IntegrationCronTriggerTargetSettings.from_dict(d.pop("settings"))

        integration_cron_trigger_target = cls(
            type_=type_,
            integration_id=integration_id,
            settings=settings,
        )

        return integration_cron_trigger_target
