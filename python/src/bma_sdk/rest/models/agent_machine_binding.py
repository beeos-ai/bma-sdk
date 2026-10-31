import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_machine_binding_kind import (
    AgentMachineBindingKind,
    check_agent_machine_binding_kind,
)
from ..models.agent_machine_binding_state import (
    AgentMachineBindingState,
    check_agent_machine_binding_state,
)

if TYPE_CHECKING:
    from ..models.agent_machine_binding_env_overlay import AgentMachineBindingEnvOverlay
    from ..models.agent_machine_binding_secret_env_overlay import (
        AgentMachineBindingSecretEnvOverlay,
    )


T = TypeVar("T", bound="AgentMachineBinding")


@_attrs_define
class AgentMachineBinding:
    """
    Attributes:
        id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):
        machine_id (str): Machine ID (mch_...).
        binding_kind (AgentMachineBindingKind):
        state (AgentMachineBindingState):
        description (str):
        cwd (str):
        env_overlay (AgentMachineBindingEnvOverlay): Env overlay applied to processes launched through this binding. For
            pool bindings it is also applied to the machine environment when the pool machine is provisioned, so the
            provider_options startup_script and the daemon run with it; connected machines keep their own environment. A
            null entry removes the key.
        secret_env_overlay (AgentMachineBindingSecretEnvOverlay): Secret env overlay applied to processes launched
            through this binding. For pool bindings it is also applied to the machine environment when the pool machine is
            provisioned, so the provider_options startup_script and the daemon run with it; connected machines keep their
            own environment. A null entry removes the key.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    project_id: str
    agent_id: str
    machine_id: str
    binding_kind: AgentMachineBindingKind
    state: AgentMachineBindingState
    description: str
    cwd: str
    env_overlay: "AgentMachineBindingEnvOverlay"
    secret_env_overlay: "AgentMachineBindingSecretEnvOverlay"
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        agent_id = self.agent_id

        machine_id = self.machine_id

        binding_kind: str = self.binding_kind

        state: str = self.state

        description = self.description

        cwd = self.cwd

        env_overlay = self.env_overlay.to_dict()

        secret_env_overlay = self.secret_env_overlay.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "agent_id": agent_id,
                "machine_id": machine_id,
                "binding_kind": binding_kind,
                "state": state,
                "description": description,
                "cwd": cwd,
                "env_overlay": env_overlay,
                "secret_env_overlay": secret_env_overlay,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_machine_binding_env_overlay import (
            AgentMachineBindingEnvOverlay,
        )
        from ..models.agent_machine_binding_secret_env_overlay import (
            AgentMachineBindingSecretEnvOverlay,
        )

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        machine_id = d.pop("machine_id")

        binding_kind = check_agent_machine_binding_kind(d.pop("binding_kind"))

        state = check_agent_machine_binding_state(d.pop("state"))

        description = d.pop("description")

        cwd = d.pop("cwd")

        env_overlay = AgentMachineBindingEnvOverlay.from_dict(d.pop("env_overlay"))

        secret_env_overlay = AgentMachineBindingSecretEnvOverlay.from_dict(
            d.pop("secret_env_overlay")
        )

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        agent_machine_binding = cls(
            id=id,
            project_id=project_id,
            agent_id=agent_id,
            machine_id=machine_id,
            binding_kind=binding_kind,
            state=state,
            description=description,
            cwd=cwd,
            env_overlay=env_overlay,
            secret_env_overlay=secret_env_overlay,
            created_at=created_at,
            updated_at=updated_at,
        )

        return agent_machine_binding
