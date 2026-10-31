from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_capabilities_tools import IntegrationCapabilitiesTools
    from ..models.integration_capability_definition import (
        IntegrationCapabilityDefinition,
    )
    from ..models.integration_subscription_definition import (
        IntegrationSubscriptionDefinition,
    )


T = TypeVar("T", bound="IntegrationCapabilities")


@_attrs_define
class IntegrationCapabilities:
    """
    Attributes:
        tools (IntegrationCapabilitiesTools):
        settings (Union[Unset, IntegrationCapabilityDefinition]):
        subscription (Union[Unset, IntegrationSubscriptionDefinition]):
        interaction_handler (Union[Unset, IntegrationCapabilityDefinition]):
        schedule (Union[Unset, IntegrationCapabilityDefinition]):
    """

    tools: "IntegrationCapabilitiesTools"
    settings: Union[Unset, "IntegrationCapabilityDefinition"] = UNSET
    subscription: Union[Unset, "IntegrationSubscriptionDefinition"] = UNSET
    interaction_handler: Union[Unset, "IntegrationCapabilityDefinition"] = UNSET
    schedule: Union[Unset, "IntegrationCapabilityDefinition"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        tools = self.tools.to_dict()

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        subscription: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.subscription, Unset):
            subscription = self.subscription.to_dict()

        interaction_handler: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interaction_handler, Unset):
            interaction_handler = self.interaction_handler.to_dict()

        schedule: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tools": tools,
            }
        )
        if settings is not UNSET:
            field_dict["settings"] = settings
        if subscription is not UNSET:
            field_dict["subscription"] = subscription
        if interaction_handler is not UNSET:
            field_dict["interaction_handler"] = interaction_handler
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_capabilities_tools import IntegrationCapabilitiesTools
        from ..models.integration_capability_definition import (
            IntegrationCapabilityDefinition,
        )
        from ..models.integration_subscription_definition import (
            IntegrationSubscriptionDefinition,
        )

        d = dict(src_dict)
        tools = IntegrationCapabilitiesTools.from_dict(d.pop("tools"))

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, IntegrationCapabilityDefinition]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = IntegrationCapabilityDefinition.from_dict(_settings)

        _subscription = d.pop("subscription", UNSET)
        subscription: Union[Unset, IntegrationSubscriptionDefinition]
        if isinstance(_subscription, Unset):
            subscription = UNSET
        else:
            subscription = IntegrationSubscriptionDefinition.from_dict(_subscription)

        _interaction_handler = d.pop("interaction_handler", UNSET)
        interaction_handler: Union[Unset, IntegrationCapabilityDefinition]
        if isinstance(_interaction_handler, Unset):
            interaction_handler = UNSET
        else:
            interaction_handler = IntegrationCapabilityDefinition.from_dict(
                _interaction_handler
            )

        _schedule = d.pop("schedule", UNSET)
        schedule: Union[Unset, IntegrationCapabilityDefinition]
        if isinstance(_schedule, Unset):
            schedule = UNSET
        else:
            schedule = IntegrationCapabilityDefinition.from_dict(_schedule)

        integration_capabilities = cls(
            tools=tools,
            settings=settings,
            subscription=subscription,
            interaction_handler=interaction_handler,
            schedule=schedule,
        )

        return integration_capabilities
