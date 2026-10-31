import datetime
from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DesktopStream")


@_attrs_define
class DesktopStream:
    """
    Attributes:
        type_ (Literal['bma.desktop_stream']):
        session_id (str):
        desktop_session_id (str):
        machine_id (str):
        url (str): WebSocket endpoint the ticket belongs to.
        ticket (str): Single-use credential. Treat as a secret.
        subprotocol (str):
        expires_at (datetime.datetime):
        permissions (list[str]):
    """

    type_: Literal["bma.desktop_stream"]
    session_id: str
    desktop_session_id: str
    machine_id: str
    url: str
    ticket: str
    subprotocol: str
    expires_at: datetime.datetime
    permissions: list[str]

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        session_id = self.session_id

        desktop_session_id = self.desktop_session_id

        machine_id = self.machine_id

        url = self.url

        ticket = self.ticket

        subprotocol = self.subprotocol

        expires_at = self.expires_at.isoformat()

        permissions = self.permissions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "session_id": session_id,
                "desktop_session_id": desktop_session_id,
                "machine_id": machine_id,
                "url": url,
                "ticket": ticket,
                "subprotocol": subprotocol,
                "expires_at": expires_at,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["bma.desktop_stream"], d.pop("type"))
        if type_ != "bma.desktop_stream":
            raise ValueError(
                f"type must match const 'bma.desktop_stream', got '{type_}'"
            )

        session_id = d.pop("session_id")

        desktop_session_id = d.pop("desktop_session_id")

        machine_id = d.pop("machine_id")

        url = d.pop("url")

        ticket = d.pop("ticket")

        subprotocol = d.pop("subprotocol")

        expires_at = isoparse(d.pop("expires_at"))

        permissions = cast(list[str], d.pop("permissions"))

        desktop_stream = cls(
            type_=type_,
            session_id=session_id,
            desktop_session_id=desktop_session_id,
            machine_id=machine_id,
            url=url,
            ticket=ticket,
            subprotocol=subprotocol,
            expires_at=expires_at,
            permissions=permissions,
        )

        return desktop_stream
