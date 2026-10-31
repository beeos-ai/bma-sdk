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
    from ..models.compiled_agent_config_interaction_handlers import (
        CompiledAgentConfigInteractionHandlers,
    )
    from ..models.compiled_agent_config_mcp import CompiledAgentConfigMcp
    from ..models.compiled_agent_config_subagents import CompiledAgentConfigSubagents
    from ..models.compiled_agent_config_tools import CompiledAgentConfigTools
    from ..models.compiled_agent_model import CompiledAgentModel
    from ..models.compiled_git_credentials import CompiledGitCredentials
    from ..models.compiled_machine_source import CompiledMachineSource
    from ..models.compiled_memory_store import CompiledMemoryStore
    from ..models.compiled_skill import CompiledSkill


T = TypeVar("T", bound="CompiledAgentConfig")


@_attrs_define
class CompiledAgentConfig:
    """Read-only saved compiled configuration, including default tools and derived subagent overrides.

    Attributes:
        instruction (str):
        model (CompiledAgentModel):
        version (Union[Unset, str]):
        machine_sources (Union[Unset, list['CompiledMachineSource']]):
        tools (Union[Unset, CompiledAgentConfigTools]):
        mcp (Union[Unset, CompiledAgentConfigMcp]):
        interaction_handlers (Union[Unset, CompiledAgentConfigInteractionHandlers]):
        git_credentials (Union[Unset, CompiledGitCredentials]): Pinned GitHub integration supplying machine Git
            credentials, optionally limited to repositories and read-only access.
        skills (Union[Unset, list['CompiledSkill']]):
        memory_stores (Union[Unset, list['CompiledMemoryStore']]):
        subagents (Union[Unset, CompiledAgentConfigSubagents]):
        max_subagents (Union[Unset, int]):
        max_depth (Union[Unset, int]):
    """

    instruction: str
    model: "CompiledAgentModel"
    version: Union[Unset, str] = UNSET
    machine_sources: Union[Unset, list["CompiledMachineSource"]] = UNSET
    tools: Union[Unset, "CompiledAgentConfigTools"] = UNSET
    mcp: Union[Unset, "CompiledAgentConfigMcp"] = UNSET
    interaction_handlers: Union[Unset, "CompiledAgentConfigInteractionHandlers"] = UNSET
    git_credentials: Union[Unset, "CompiledGitCredentials"] = UNSET
    skills: Union[Unset, list["CompiledSkill"]] = UNSET
    memory_stores: Union[Unset, list["CompiledMemoryStore"]] = UNSET
    subagents: Union[Unset, "CompiledAgentConfigSubagents"] = UNSET
    max_subagents: Union[Unset, int] = UNSET
    max_depth: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        instruction = self.instruction

        model = self.model.to_dict()

        version = self.version

        machine_sources: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.machine_sources, Unset):
            machine_sources = []
            for machine_sources_item_data in self.machine_sources:
                machine_sources_item = machine_sources_item_data.to_dict()
                machine_sources.append(machine_sources_item)

        tools: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools.to_dict()

        mcp: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.mcp, Unset):
            mcp = self.mcp.to_dict()

        interaction_handlers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interaction_handlers, Unset):
            interaction_handlers = self.interaction_handlers.to_dict()

        git_credentials: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.git_credentials, Unset):
            git_credentials = self.git_credentials.to_dict()

        skills: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.skills, Unset):
            skills = []
            for skills_item_data in self.skills:
                skills_item = skills_item_data.to_dict()
                skills.append(skills_item)

        memory_stores: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.memory_stores, Unset):
            memory_stores = []
            for memory_stores_item_data in self.memory_stores:
                memory_stores_item = memory_stores_item_data.to_dict()
                memory_stores.append(memory_stores_item)

        subagents: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.subagents, Unset):
            subagents = self.subagents.to_dict()

        max_subagents = self.max_subagents

        max_depth = self.max_depth

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "instruction": instruction,
                "model": model,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if machine_sources is not UNSET:
            field_dict["machine_sources"] = machine_sources
        if tools is not UNSET:
            field_dict["tools"] = tools
        if mcp is not UNSET:
            field_dict["mcp"] = mcp
        if interaction_handlers is not UNSET:
            field_dict["interaction_handlers"] = interaction_handlers
        if git_credentials is not UNSET:
            field_dict["git_credentials"] = git_credentials
        if skills is not UNSET:
            field_dict["skills"] = skills
        if memory_stores is not UNSET:
            field_dict["memory_stores"] = memory_stores
        if subagents is not UNSET:
            field_dict["subagents"] = subagents
        if max_subagents is not UNSET:
            field_dict["max_subagents"] = max_subagents
        if max_depth is not UNSET:
            field_dict["max_depth"] = max_depth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_agent_config_interaction_handlers import (
            CompiledAgentConfigInteractionHandlers,
        )
        from ..models.compiled_agent_config_mcp import CompiledAgentConfigMcp
        from ..models.compiled_agent_config_subagents import (
            CompiledAgentConfigSubagents,
        )
        from ..models.compiled_agent_config_tools import CompiledAgentConfigTools
        from ..models.compiled_agent_model import CompiledAgentModel
        from ..models.compiled_git_credentials import CompiledGitCredentials
        from ..models.compiled_machine_source import CompiledMachineSource
        from ..models.compiled_memory_store import CompiledMemoryStore
        from ..models.compiled_skill import CompiledSkill

        d = dict(src_dict)
        instruction = d.pop("instruction")

        model = CompiledAgentModel.from_dict(d.pop("model"))

        version = d.pop("version", UNSET)

        machine_sources = []
        _machine_sources = d.pop("machine_sources", UNSET)
        for machine_sources_item_data in _machine_sources or []:
            machine_sources_item = CompiledMachineSource.from_dict(
                machine_sources_item_data
            )

            machine_sources.append(machine_sources_item)

        _tools = d.pop("tools", UNSET)
        tools: Union[Unset, CompiledAgentConfigTools]
        if isinstance(_tools, Unset):
            tools = UNSET
        else:
            tools = CompiledAgentConfigTools.from_dict(_tools)

        _mcp = d.pop("mcp", UNSET)
        mcp: Union[Unset, CompiledAgentConfigMcp]
        if isinstance(_mcp, Unset):
            mcp = UNSET
        else:
            mcp = CompiledAgentConfigMcp.from_dict(_mcp)

        _interaction_handlers = d.pop("interaction_handlers", UNSET)
        interaction_handlers: Union[Unset, CompiledAgentConfigInteractionHandlers]
        if isinstance(_interaction_handlers, Unset):
            interaction_handlers = UNSET
        else:
            interaction_handlers = CompiledAgentConfigInteractionHandlers.from_dict(
                _interaction_handlers
            )

        _git_credentials = d.pop("git_credentials", UNSET)
        git_credentials: Union[Unset, CompiledGitCredentials]
        if isinstance(_git_credentials, Unset):
            git_credentials = UNSET
        else:
            git_credentials = CompiledGitCredentials.from_dict(_git_credentials)

        skills = []
        _skills = d.pop("skills", UNSET)
        for skills_item_data in _skills or []:
            skills_item = CompiledSkill.from_dict(skills_item_data)

            skills.append(skills_item)

        memory_stores = []
        _memory_stores = d.pop("memory_stores", UNSET)
        for memory_stores_item_data in _memory_stores or []:
            memory_stores_item = CompiledMemoryStore.from_dict(memory_stores_item_data)

            memory_stores.append(memory_stores_item)

        _subagents = d.pop("subagents", UNSET)
        subagents: Union[Unset, CompiledAgentConfigSubagents]
        if isinstance(_subagents, Unset):
            subagents = UNSET
        else:
            subagents = CompiledAgentConfigSubagents.from_dict(_subagents)

        max_subagents = d.pop("max_subagents", UNSET)

        max_depth = d.pop("max_depth", UNSET)

        compiled_agent_config = cls(
            instruction=instruction,
            model=model,
            version=version,
            machine_sources=machine_sources,
            tools=tools,
            mcp=mcp,
            interaction_handlers=interaction_handlers,
            git_credentials=git_credentials,
            skills=skills,
            memory_stores=memory_stores,
            subagents=subagents,
            max_subagents=max_subagents,
            max_depth=max_depth,
        )

        return compiled_agent_config
