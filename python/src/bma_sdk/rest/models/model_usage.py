from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelUsage")


@_attrs_define
class ModelUsage:
    """Token counts the provider reported for one model call. Cache and reasoning counts are omitted when the provider
    reported none.

        Attributes:
            input_tokens_total (Union[Unset, int]):
            uncached_input_tokens (Union[Unset, int]):
            output_tokens_total (Union[Unset, int]):
            reasoning_output_tokens (Union[Unset, int]):
            cache_read_input_tokens (Union[Unset, int]):
            cache_write_input_tokens (Union[Unset, int]):
    """

    input_tokens_total: Union[Unset, int] = UNSET
    uncached_input_tokens: Union[Unset, int] = UNSET
    output_tokens_total: Union[Unset, int] = UNSET
    reasoning_output_tokens: Union[Unset, int] = UNSET
    cache_read_input_tokens: Union[Unset, int] = UNSET
    cache_write_input_tokens: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        input_tokens_total = self.input_tokens_total

        uncached_input_tokens = self.uncached_input_tokens

        output_tokens_total = self.output_tokens_total

        reasoning_output_tokens = self.reasoning_output_tokens

        cache_read_input_tokens = self.cache_read_input_tokens

        cache_write_input_tokens = self.cache_write_input_tokens

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if input_tokens_total is not UNSET:
            field_dict["input_tokens_total"] = input_tokens_total
        if uncached_input_tokens is not UNSET:
            field_dict["uncached_input_tokens"] = uncached_input_tokens
        if output_tokens_total is not UNSET:
            field_dict["output_tokens_total"] = output_tokens_total
        if reasoning_output_tokens is not UNSET:
            field_dict["reasoning_output_tokens"] = reasoning_output_tokens
        if cache_read_input_tokens is not UNSET:
            field_dict["cache_read_input_tokens"] = cache_read_input_tokens
        if cache_write_input_tokens is not UNSET:
            field_dict["cache_write_input_tokens"] = cache_write_input_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens_total = d.pop("input_tokens_total", UNSET)

        uncached_input_tokens = d.pop("uncached_input_tokens", UNSET)

        output_tokens_total = d.pop("output_tokens_total", UNSET)

        reasoning_output_tokens = d.pop("reasoning_output_tokens", UNSET)

        cache_read_input_tokens = d.pop("cache_read_input_tokens", UNSET)

        cache_write_input_tokens = d.pop("cache_write_input_tokens", UNSET)

        model_usage = cls(
            input_tokens_total=input_tokens_total,
            uncached_input_tokens=uncached_input_tokens,
            output_tokens_total=output_tokens_total,
            reasoning_output_tokens=reasoning_output_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_write_input_tokens=cache_write_input_tokens,
        )

        return model_usage
