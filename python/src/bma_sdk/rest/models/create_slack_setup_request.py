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
    from ..models.slack_setup_icon import SlackSetupIcon


T = TypeVar("T", bound="CreateSlackSetupRequest")


@_attrs_define
class CreateSlackSetupRequest:
    """
    Attributes:
        app_name (str):
        app_configuration_token (str):
        icon (Union[Unset, SlackSetupIcon]):
        return_to (Union[Unset, str]):
    """

    app_name: str
    app_configuration_token: str
    icon: Union[Unset, "SlackSetupIcon"] = UNSET
    return_to: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        app_name = self.app_name

        app_configuration_token = self.app_configuration_token

        icon: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.icon, Unset):
            icon = self.icon.to_dict()

        return_to = self.return_to

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "app_name": app_name,
                "app_configuration_token": app_configuration_token,
            }
        )
        if icon is not UNSET:
            field_dict["icon"] = icon
        if return_to is not UNSET:
            field_dict["return_to"] = return_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slack_setup_icon import SlackSetupIcon

        d = dict(src_dict)
        app_name = d.pop("app_name")

        app_configuration_token = d.pop("app_configuration_token")

        _icon = d.pop("icon", UNSET)
        icon: Union[Unset, SlackSetupIcon]
        if isinstance(_icon, Unset):
            icon = UNSET
        else:
            icon = SlackSetupIcon.from_dict(_icon)

        return_to = d.pop("return_to", UNSET)

        create_slack_setup_request = cls(
            app_name=app_name,
            app_configuration_token=app_configuration_token,
            icon=icon,
            return_to=return_to,
        )

        return create_slack_setup_request
