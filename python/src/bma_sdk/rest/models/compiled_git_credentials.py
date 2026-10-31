from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompiledGitCredentials")


@_attrs_define
class CompiledGitCredentials:
    """Pinned GitHub integration supplying machine Git credentials, optionally limited to repositories and read-only
    access.

        Attributes:
            integration (str): Immutable, project-unique integration name used in config keys and qualified tool names.
            integration_id (str):
            repository_ids (Union[Unset, list[int]]):
            read_only (Union[Unset, bool]):
    """

    integration: str
    integration_id: str
    repository_ids: Union[Unset, list[int]] = UNSET
    read_only: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        integration = self.integration

        integration_id = self.integration_id

        repository_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.repository_ids, Unset):
            repository_ids = self.repository_ids

        read_only = self.read_only

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration": integration,
                "integration_id": integration_id,
            }
        )
        if repository_ids is not UNSET:
            field_dict["repository_ids"] = repository_ids
        if read_only is not UNSET:
            field_dict["read_only"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration = d.pop("integration")

        integration_id = d.pop("integration_id")

        repository_ids = cast(list[int], d.pop("repository_ids", UNSET))

        read_only = d.pop("read_only", UNSET)

        compiled_git_credentials = cls(
            integration=integration,
            integration_id=integration_id,
            repository_ids=repository_ids,
            read_only=read_only,
        )

        return compiled_git_credentials
