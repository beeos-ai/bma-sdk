from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.daemon_runtime import DaemonRuntime
    from ..models.daemon_runtime_reconciliation import DaemonRuntimeReconciliation


T = TypeVar("T", bound="RegisterDaemonRuntimeResponse")


@_attrs_define
class RegisterDaemonRuntimeResponse:
    """
    Attributes:
        runtime (DaemonRuntime):
        reconciliation (DaemonRuntimeReconciliation):
    """

    runtime: "DaemonRuntime"
    reconciliation: "DaemonRuntimeReconciliation"

    def to_dict(self) -> dict[str, Any]:
        runtime = self.runtime.to_dict()

        reconciliation = self.reconciliation.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "runtime": runtime,
                "reconciliation": reconciliation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daemon_runtime import DaemonRuntime
        from ..models.daemon_runtime_reconciliation import DaemonRuntimeReconciliation

        d = dict(src_dict)
        runtime = DaemonRuntime.from_dict(d.pop("runtime"))

        reconciliation = DaemonRuntimeReconciliation.from_dict(d.pop("reconciliation"))

        register_daemon_runtime_response = cls(
            runtime=runtime,
            reconciliation=reconciliation,
        )

        return register_daemon_runtime_response
