from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigDefinitionGitCredentials")


@_attrs_define
class AgentConfigDefinitionGitCredentials:
    """Integration whose git credentials the agent's machines use.

    Attributes:
        integration (str):
        repository_ids (Union[Unset, list[int]]): GitHub repository IDs the credentials can access. Defaults to every
            repository the installation can access.
        read_only (Union[Unset, bool]): Prevents pushing, even if the integration allows it.
    """

    integration: str
    repository_ids: Union[Unset, list[int]] = UNSET
    read_only: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        integration = self.integration

        repository_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.repository_ids, Unset):
            repository_ids = self.repository_ids

        read_only = self.read_only

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration": integration,
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

        repository_ids = cast(list[int], d.pop("repository_ids", UNSET))

        read_only = d.pop("read_only", UNSET)

        agent_config_definition_git_credentials = cls(
            integration=integration,
            repository_ids=repository_ids,
            read_only=read_only,
        )

        return agent_config_definition_git_credentials
