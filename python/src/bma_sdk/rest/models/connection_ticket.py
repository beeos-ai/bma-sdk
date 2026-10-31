import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.connection_ticket_purpose import (
    ConnectionTicketPurpose,
    check_connection_ticket_purpose,
)

T = TypeVar("T", bound="ConnectionTicket")


@_attrs_define
class ConnectionTicket:
    """
    Attributes:
        id (str): Connection ticket ID (tkt_...).
        ticket (str): Opaque single-use ticket. Returned once and never logged.
        purpose (ConnectionTicketPurpose):
        expires_at (datetime.datetime):
        ws_url (str): WebSocket URL without the ticket.
        subprotocol (str):
        permissions (list[str]):
    """

    id: str
    ticket: str
    purpose: ConnectionTicketPurpose
    expires_at: datetime.datetime
    ws_url: str
    subprotocol: str
    permissions: list[str]

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ticket = self.ticket

        purpose: str = self.purpose

        expires_at = self.expires_at.isoformat()

        ws_url = self.ws_url

        subprotocol = self.subprotocol

        permissions = self.permissions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "ticket": ticket,
                "purpose": purpose,
                "expires_at": expires_at,
                "ws_url": ws_url,
                "subprotocol": subprotocol,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        ticket = d.pop("ticket")

        purpose = check_connection_ticket_purpose(d.pop("purpose"))

        expires_at = isoparse(d.pop("expires_at"))

        ws_url = d.pop("ws_url")

        subprotocol = d.pop("subprotocol")

        permissions = cast(list[str], d.pop("permissions"))

        connection_ticket = cls(
            id=id,
            ticket=ticket,
            purpose=purpose,
            expires_at=expires_at,
            ws_url=ws_url,
            subprotocol=subprotocol,
            permissions=permissions,
        )

        return connection_ticket
