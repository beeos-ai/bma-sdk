from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_executor_binding import AgentExecutorBinding


T = TypeVar("T", bound="AgentExecutorBindingEnvelope")


@_attrs_define
class AgentExecutorBindingEnvelope:
    """
    Attributes:
        executor_binding (AgentExecutorBinding):
    """

    executor_binding: "AgentExecutorBinding"

    def to_dict(self) -> dict[str, Any]:
        executor_binding = self.executor_binding.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "executor_binding": executor_binding,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_executor_binding import AgentExecutorBinding

        d = dict(src_dict)
        executor_binding = AgentExecutorBinding.from_dict(d.pop("executor_binding"))

        agent_executor_binding_envelope = cls(
            executor_binding=executor_binding,
        )

        return agent_executor_binding_envelope
