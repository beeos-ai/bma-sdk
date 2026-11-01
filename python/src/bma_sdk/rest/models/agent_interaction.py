import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_interaction_kind import (
    AgentInteractionKind,
    check_agent_interaction_kind,
)
from ..models.agent_interaction_state import (
    AgentInteractionState,
    check_agent_interaction_state,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_interaction_destination import AgentInteractionDestination
    from ..models.interaction_form import InteractionForm
    from ..models.interaction_presentation_receipt import InteractionPresentationReceipt
    from ..models.interaction_resolution import InteractionResolution


T = TypeVar("T", bound="AgentInteraction")


@_attrs_define
class AgentInteraction:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):
        tool_call_id (str):
        interaction_kind (AgentInteractionKind):
        state (AgentInteractionState):
        request (InteractionForm):
        created_at (datetime.datetime):
        tool_use_id (Union[Unset, str]): For an approval raised by an agent executor, the id of the agent.tool_use event
            it refers to (tool_call_id then identifies the approval itself). Absent for native tool calls.
        tool_name (Union[Unset, str]): The tool whose invocation a permission interaction guards. Present only when
            interaction_kind is permission.
        agent_name (Union[Unset, str]): Agent name. Empty means the agent is unnamed; non-empty values use the
            ResourceName policy.
        subagent_key (Union[Unset, str]): Present when the interaction belongs to a subagent of the listed agent.
        resolution (Union[Unset, InteractionResolution]):
        destination (Union[Unset, AgentInteractionDestination]): Immutable handler and destination captured when the
            interaction was created. Provider delivery and callbacks check current integration and handler authority.
            Dashboard/API resolution remains available independently.
        presentation_receipt (Union[Unset, InteractionPresentationReceipt]): Confirmed provider presentation metadata,
            when recorded. This is not an execution grant or a delivery guarantee. Absence does not prove a remote send
            failed. Customer-hosted presenters maintain their own delivery records.
        resolved_by_input_id (Union[Unset, str]):
        resolved_at (Union[Unset, datetime.datetime]):
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    tool_call_id: str
    interaction_kind: AgentInteractionKind
    state: AgentInteractionState
    request: "InteractionForm"
    created_at: datetime.datetime
    tool_use_id: Union[Unset, str] = UNSET
    tool_name: Union[Unset, str] = UNSET
    agent_name: Union[Unset, str] = UNSET
    subagent_key: Union[Unset, str] = UNSET
    resolution: Union[Unset, "InteractionResolution"] = UNSET
    destination: Union[Unset, "AgentInteractionDestination"] = UNSET
    presentation_receipt: Union[Unset, "InteractionPresentationReceipt"] = UNSET
    resolved_by_input_id: Union[Unset, str] = UNSET
    resolved_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        tool_call_id = self.tool_call_id

        interaction_kind: str = self.interaction_kind

        state: str = self.state

        request = self.request.to_dict()

        created_at = self.created_at.isoformat()

        tool_use_id = self.tool_use_id

        tool_name = self.tool_name

        agent_name = self.agent_name

        subagent_key = self.subagent_key

        resolution: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resolution, Unset):
            resolution = self.resolution.to_dict()

        destination: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.destination, Unset):
            destination = self.destination.to_dict()

        presentation_receipt: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.presentation_receipt, Unset):
            presentation_receipt = self.presentation_receipt.to_dict()

        resolved_by_input_id = self.resolved_by_input_id

        resolved_at: Union[Unset, str] = UNSET
        if not isinstance(self.resolved_at, Unset):
            resolved_at = self.resolved_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "agent_id": agent_id,
                "tool_call_id": tool_call_id,
                "interaction_kind": interaction_kind,
                "state": state,
                "request": request,
                "created_at": created_at,
            }
        )
        if tool_use_id is not UNSET:
            field_dict["tool_use_id"] = tool_use_id
        if tool_name is not UNSET:
            field_dict["tool_name"] = tool_name
        if agent_name is not UNSET:
            field_dict["agent_name"] = agent_name
        if subagent_key is not UNSET:
            field_dict["subagent_key"] = subagent_key
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if destination is not UNSET:
            field_dict["destination"] = destination
        if presentation_receipt is not UNSET:
            field_dict["presentation_receipt"] = presentation_receipt
        if resolved_by_input_id is not UNSET:
            field_dict["resolved_by_input_id"] = resolved_by_input_id
        if resolved_at is not UNSET:
            field_dict["resolved_at"] = resolved_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_interaction_destination import AgentInteractionDestination
        from ..models.interaction_form import InteractionForm
        from ..models.interaction_presentation_receipt import (
            InteractionPresentationReceipt,
        )
        from ..models.interaction_resolution import InteractionResolution

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        tool_call_id = d.pop("tool_call_id")

        interaction_kind = check_agent_interaction_kind(d.pop("interaction_kind"))

        state = check_agent_interaction_state(d.pop("state"))

        request = InteractionForm.from_dict(d.pop("request"))

        created_at = isoparse(d.pop("created_at"))

        tool_use_id = d.pop("tool_use_id", UNSET)

        tool_name = d.pop("tool_name", UNSET)

        agent_name = d.pop("agent_name", UNSET)

        subagent_key = d.pop("subagent_key", UNSET)

        _resolution = d.pop("resolution", UNSET)
        resolution: Union[Unset, InteractionResolution]
        if isinstance(_resolution, Unset):
            resolution = UNSET
        else:
            resolution = InteractionResolution.from_dict(_resolution)

        _destination = d.pop("destination", UNSET)
        destination: Union[Unset, AgentInteractionDestination]
        if isinstance(_destination, Unset):
            destination = UNSET
        else:
            destination = AgentInteractionDestination.from_dict(_destination)

        _presentation_receipt = d.pop("presentation_receipt", UNSET)
        presentation_receipt: Union[Unset, InteractionPresentationReceipt]
        if isinstance(_presentation_receipt, Unset):
            presentation_receipt = UNSET
        else:
            presentation_receipt = InteractionPresentationReceipt.from_dict(
                _presentation_receipt
            )

        resolved_by_input_id = d.pop("resolved_by_input_id", UNSET)

        _resolved_at = d.pop("resolved_at", UNSET)
        resolved_at: Union[Unset, datetime.datetime]
        if isinstance(_resolved_at, Unset):
            resolved_at = UNSET
        else:
            resolved_at = isoparse(_resolved_at)

        agent_interaction = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            tool_call_id=tool_call_id,
            interaction_kind=interaction_kind,
            state=state,
            request=request,
            created_at=created_at,
            tool_use_id=tool_use_id,
            tool_name=tool_name,
            agent_name=agent_name,
            subagent_key=subagent_key,
            resolution=resolution,
            destination=destination,
            presentation_receipt=presentation_receipt,
            resolved_by_input_id=resolved_by_input_id,
            resolved_at=resolved_at,
        )

        return agent_interaction
