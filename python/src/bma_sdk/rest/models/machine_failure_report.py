import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.machine_failure_report_stage import (
    MachineFailureReportStage,
    check_machine_failure_report_stage,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MachineFailureReport")


@_attrs_define
class MachineFailureReport:
    """The machine's most recent daemon-reported failure. A single slot, overwritten by newer reports. Runtime crash
    reports remain as historical diagnostics; recovery may clear other failure stages.

        Attributes:
            stage (MachineFailureReportStage):
            output_tail (str):
            output_truncated (bool):
            reported_at (datetime.datetime):
            exit_status (Union[Unset, int]):
            daemon_version (Union[Unset, str]):
            target_version (Union[Unset, str]):
    """

    stage: MachineFailureReportStage
    output_tail: str
    output_truncated: bool
    reported_at: datetime.datetime
    exit_status: Union[Unset, int] = UNSET
    daemon_version: Union[Unset, str] = UNSET
    target_version: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        stage: str = self.stage

        output_tail = self.output_tail

        output_truncated = self.output_truncated

        reported_at = self.reported_at.isoformat()

        exit_status = self.exit_status

        daemon_version = self.daemon_version

        target_version = self.target_version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "stage": stage,
                "output_tail": output_tail,
                "output_truncated": output_truncated,
                "reported_at": reported_at,
            }
        )
        if exit_status is not UNSET:
            field_dict["exit_status"] = exit_status
        if daemon_version is not UNSET:
            field_dict["daemon_version"] = daemon_version
        if target_version is not UNSET:
            field_dict["target_version"] = target_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stage = check_machine_failure_report_stage(d.pop("stage"))

        output_tail = d.pop("output_tail")

        output_truncated = d.pop("output_truncated")

        reported_at = isoparse(d.pop("reported_at"))

        exit_status = d.pop("exit_status", UNSET)

        daemon_version = d.pop("daemon_version", UNSET)

        target_version = d.pop("target_version", UNSET)

        machine_failure_report = cls(
            stage=stage,
            output_tail=output_tail,
            output_truncated=output_truncated,
            reported_at=reported_at,
            exit_status=exit_status,
            daemon_version=daemon_version,
            target_version=target_version,
        )

        return machine_failure_report
