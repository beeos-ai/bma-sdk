from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateAgentProfileRequest")


@_attrs_define
class UpdateAgentProfileRequest:
    """
    Attributes:
        config (str): Agent config ID (acfg_...).
        expected_current_config_id (str): Agent config ID (acfg_...).
    """

    config: str
    expected_current_config_id: str

    def to_dict(self) -> dict[str, Any]:
        config = self.config

        expected_current_config_id = self.expected_current_config_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "config": config,
                "expected_current_config_id": expected_current_config_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config = d.pop("config")

        expected_current_config_id = d.pop("expected_current_config_id")

        update_agent_profile_request = cls(
            config=config,
            expected_current_config_id=expected_current_config_id,
        )

        return update_agent_profile_request
