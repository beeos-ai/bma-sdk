from typing import Literal, cast

ConnectionTicketPurpose = Literal["desktop_watch", "terminal_connect"]

CONNECTION_TICKET_PURPOSE_VALUES: set[ConnectionTicketPurpose] = {
    "desktop_watch",
    "terminal_connect",
}


def check_connection_ticket_purpose(value: str) -> ConnectionTicketPurpose:
    if value in CONNECTION_TICKET_PURPOSE_VALUES:
        return cast(ConnectionTicketPurpose, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CONNECTION_TICKET_PURPOSE_VALUES!r}"
    )
