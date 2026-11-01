from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_executor_binding_capability_type_0 import (
        AgentExecutorBindingCapabilityType0,
    )


T = TypeVar("T", bound="AgentExecutorBinding")


@_attrs_define
class AgentExecutorBinding:
    """
    Attributes:
        agent_id (str):
        machine_id (str): Machine ID (mch_...).
        capability (Union['AgentExecutorBindingCapabilityType0', None]): capabilities.agent from the machine executor's
            latest executor.register, or null before an agent executor has registered.
    """

    agent_id: str
    machine_id: str
    capability: Union["AgentExecutorBindingCapabilityType0", None]

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_executor_binding_capability_type_0 import (
            AgentExecutorBindingCapabilityType0,
        )

        agent_id = self.agent_id

        machine_id = self.machine_id

        capability: Union[None, dict[str, Any]]
        if isinstance(self.capability, AgentExecutorBindingCapabilityType0):
            capability = self.capability.to_dict()
        else:
            capability = self.capability

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_id": agent_id,
                "machine_id": machine_id,
                "capability": capability,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_executor_binding_capability_type_0 import (
            AgentExecutorBindingCapabilityType0,
        )

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        machine_id = d.pop("machine_id")

        def _parse_capability(
            data: object,
        ) -> Union["AgentExecutorBindingCapabilityType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                capability_type_0 = AgentExecutorBindingCapabilityType0.from_dict(data)

                return capability_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentExecutorBindingCapabilityType0", None], data)

        capability = _parse_capability(d.pop("capability"))

        agent_executor_binding = cls(
            agent_id=agent_id,
            machine_id=machine_id,
            capability=capability,
        )

        return agent_executor_binding
