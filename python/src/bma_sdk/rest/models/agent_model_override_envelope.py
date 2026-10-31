from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_model_override import AgentModelOverride


T = TypeVar("T", bound="AgentModelOverrideEnvelope")


@_attrs_define
class AgentModelOverrideEnvelope:
    """
    Attributes:
        model_override (AgentModelOverride):
    """

    model_override: "AgentModelOverride"

    def to_dict(self) -> dict[str, Any]:
        model_override = self.model_override.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_override": model_override,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_model_override import AgentModelOverride

        d = dict(src_dict)
        model_override = AgentModelOverride.from_dict(d.pop("model_override"))

        agent_model_override_envelope = cls(
            model_override=model_override,
        )

        return agent_model_override_envelope
