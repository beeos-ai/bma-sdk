from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelConfigOverride")


@_attrs_define
class ModelConfigOverride:
    """Session `agent.model` object with the BMA credential override. The
    `api_*` fields are write-only and never echoed. `api_url` and
    `api_format` are required when `api_key` is set.

        Attributes:
            id (str):
            effort (Union[None, Unset, str]):
            inference_geo (Union[None, Unset, str]):
            speed (Union[None, Unset, str]):
            api_url (Union[Unset, str]):
            api_key (Union[Unset, str]):
            api_format (Union[Unset, str]):
    """

    id: str
    effort: Union[None, Unset, str] = UNSET
    inference_geo: Union[None, Unset, str] = UNSET
    speed: Union[None, Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET
    api_key: Union[Unset, str] = UNSET
    api_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        effort: Union[None, Unset, str]
        if isinstance(self.effort, Unset):
            effort = UNSET
        else:
            effort = self.effort

        inference_geo: Union[None, Unset, str]
        if isinstance(self.inference_geo, Unset):
            inference_geo = UNSET
        else:
            inference_geo = self.inference_geo

        speed: Union[None, Unset, str]
        if isinstance(self.speed, Unset):
            speed = UNSET
        else:
            speed = self.speed

        api_url = self.api_url

        api_key = self.api_key

        api_format = self.api_format

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if effort is not UNSET:
            field_dict["effort"] = effort
        if inference_geo is not UNSET:
            field_dict["inference_geo"] = inference_geo
        if speed is not UNSET:
            field_dict["speed"] = speed
        if api_url is not UNSET:
            field_dict["api_url"] = api_url
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if api_format is not UNSET:
            field_dict["api_format"] = api_format

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_effort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        effort = _parse_effort(d.pop("effort", UNSET))

        def _parse_inference_geo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_geo = _parse_inference_geo(d.pop("inference_geo", UNSET))

        def _parse_speed(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        speed = _parse_speed(d.pop("speed", UNSET))

        api_url = d.pop("api_url", UNSET)

        api_key = d.pop("api_key", UNSET)

        api_format = d.pop("api_format", UNSET)

        model_config_override = cls(
            id=id,
            effort=effort,
            inference_geo=inference_geo,
            speed=speed,
            api_url=api_url,
            api_key=api_key,
            api_format=api_format,
        )

        model_config_override.additional_properties = d
        return model_config_override

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
