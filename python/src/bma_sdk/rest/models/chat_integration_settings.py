from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_integration_launcher import ChatIntegrationLauncher


T = TypeVar("T", bound="ChatIntegrationSettings")


@_attrs_define
class ChatIntegrationSettings:
    """
    Attributes:
        launcher (Union[Unset, ChatIntegrationLauncher]):
    """

    launcher: Union[Unset, "ChatIntegrationLauncher"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        launcher: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.launcher, Unset):
            launcher = self.launcher.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if launcher is not UNSET:
            field_dict["launcher"] = launcher

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_integration_launcher import ChatIntegrationLauncher

        d = dict(src_dict)
        _launcher = d.pop("launcher", UNSET)
        launcher: Union[Unset, ChatIntegrationLauncher]
        if isinstance(_launcher, Unset):
            launcher = UNSET
        else:
            launcher = ChatIntegrationLauncher.from_dict(_launcher)

        chat_integration_settings = cls(
            launcher=launcher,
        )

        return chat_integration_settings
