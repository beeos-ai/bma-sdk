import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.desktop_control_status_mode import (
    DesktopControlStatusMode,
    check_desktop_control_status_mode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DesktopControlStatus")


@_attrs_define
class DesktopControlStatus:
    """
    Attributes:
        mode (DesktopControlStatusMode):
        epoch (int):
        generation (int):
        holder (str):
        agent_state (str):
        lease_id (Union[Unset, str]):
        lease_expires_at (Union[Unset, datetime.datetime]):
    """

    mode: DesktopControlStatusMode
    epoch: int
    generation: int
    holder: str
    agent_state: str
    lease_id: Union[Unset, str] = UNSET
    lease_expires_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        mode: str = self.mode

        epoch = self.epoch

        generation = self.generation

        holder = self.holder

        agent_state = self.agent_state

        lease_id = self.lease_id

        lease_expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.lease_expires_at, Unset):
            lease_expires_at = self.lease_expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
                "epoch": epoch,
                "generation": generation,
                "holder": holder,
                "agent_state": agent_state,
            }
        )
        if lease_id is not UNSET:
            field_dict["lease_id"] = lease_id
        if lease_expires_at is not UNSET:
            field_dict["lease_expires_at"] = lease_expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = check_desktop_control_status_mode(d.pop("mode"))

        epoch = d.pop("epoch")

        generation = d.pop("generation")

        holder = d.pop("holder")

        agent_state = d.pop("agent_state")

        lease_id = d.pop("lease_id", UNSET)

        _lease_expires_at = d.pop("lease_expires_at", UNSET)
        lease_expires_at: Union[Unset, datetime.datetime]
        if isinstance(_lease_expires_at, Unset):
            lease_expires_at = UNSET
        else:
            lease_expires_at = isoparse(_lease_expires_at)

        desktop_control_status = cls(
            mode=mode,
            epoch=epoch,
            generation=generation,
            holder=holder,
            agent_state=agent_state,
            lease_id=lease_id,
            lease_expires_at=lease_expires_at,
        )

        return desktop_control_status
