from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageTokenTotals")


@_attrs_define
class UsageTokenTotals:
    """Summed token counts across the tallied model calls. Input totals are the sum of uncached, cache-read, and cache-
    write tokens; output totals include reasoning tokens.

        Attributes:
            input_tokens_total (int):
            uncached_input_tokens (int):
            cache_read_input_tokens (int):
            cache_write_input_tokens (int):
            output_tokens_total (int):
            reasoning_output_tokens (int):
    """

    input_tokens_total: int
    uncached_input_tokens: int
    cache_read_input_tokens: int
    cache_write_input_tokens: int
    output_tokens_total: int
    reasoning_output_tokens: int

    def to_dict(self) -> dict[str, Any]:
        input_tokens_total = self.input_tokens_total

        uncached_input_tokens = self.uncached_input_tokens

        cache_read_input_tokens = self.cache_read_input_tokens

        cache_write_input_tokens = self.cache_write_input_tokens

        output_tokens_total = self.output_tokens_total

        reasoning_output_tokens = self.reasoning_output_tokens

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "input_tokens_total": input_tokens_total,
                "uncached_input_tokens": uncached_input_tokens,
                "cache_read_input_tokens": cache_read_input_tokens,
                "cache_write_input_tokens": cache_write_input_tokens,
                "output_tokens_total": output_tokens_total,
                "reasoning_output_tokens": reasoning_output_tokens,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens_total = d.pop("input_tokens_total")

        uncached_input_tokens = d.pop("uncached_input_tokens")

        cache_read_input_tokens = d.pop("cache_read_input_tokens")

        cache_write_input_tokens = d.pop("cache_write_input_tokens")

        output_tokens_total = d.pop("output_tokens_total")

        reasoning_output_tokens = d.pop("reasoning_output_tokens")

        usage_token_totals = cls(
            input_tokens_total=input_tokens_total,
            uncached_input_tokens=uncached_input_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_write_input_tokens=cache_write_input_tokens,
            output_tokens_total=output_tokens_total,
            reasoning_output_tokens=reasoning_output_tokens,
        )

        return usage_token_totals
