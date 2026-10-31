from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine_daemon_token import MachineDaemonToken


T = TypeVar("T", bound="CreateMachineDaemonTokenResponse")


@_attrs_define
class CreateMachineDaemonTokenResponse:
    """
    Attributes:
        token (str): Opaque bearer credential.
        token_record (MachineDaemonToken):
    """

    token: str
    token_record: "MachineDaemonToken"

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        token_record = self.token_record.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "token": token,
                "token_record": token_record,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_daemon_token import MachineDaemonToken

        d = dict(src_dict)
        token = d.pop("token")

        token_record = MachineDaemonToken.from_dict(d.pop("token_record"))

        create_machine_daemon_token_response = cls(
            token=token,
            token_record=token_record,
        )

        return create_machine_daemon_token_response
