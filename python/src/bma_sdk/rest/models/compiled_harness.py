from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.compiled_harness_kind import (
    CompiledHarnessKind,
    check_compiled_harness_kind,
)

T = TypeVar("T", bound="CompiledHarness")


@_attrs_define
class CompiledHarness:
    """Experimental. A non-default harness; absent for the BMA harness on the server. Where it runs is not part of the
    agent config: it follows the session's machine sources.

        Attributes:
            kind (CompiledHarnessKind):
            agent (str):
    """

    kind: CompiledHarnessKind
    agent: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        agent = self.agent

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "agent": agent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_compiled_harness_kind(d.pop("kind"))

        agent = d.pop("agent")

        compiled_harness = cls(
            kind=kind,
            agent=agent,
        )

        return compiled_harness
