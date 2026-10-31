from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_git_credentials import (
        AgentConfigDefinitionGitCredentials,
    )
    from ..models.agent_config_definition_interaction_handlers_type_0 import (
        AgentConfigDefinitionInteractionHandlersType0,
    )
    from ..models.agent_config_definition_machine_source_type_0 import (
        AgentConfigDefinitionMachineSourceType0,
    )
    from ..models.agent_config_definition_machine_source_type_1 import (
        AgentConfigDefinitionMachineSourceType1,
    )
    from ..models.agent_config_definition_mcp_servers_type_0 import (
        AgentConfigDefinitionMCPServersType0,
    )
    from ..models.agent_config_definition_memory_store import (
        AgentConfigDefinitionMemoryStore,
    )
    from ..models.agent_config_definition_subagents_type_0 import (
        AgentConfigDefinitionSubagentsType0,
    )
    from ..models.agent_config_definition_tools_type_0 import (
        AgentConfigDefinitionToolsType0,
    )


T = TypeVar("T", bound="AgentConfigToolsDefinition")


@_attrs_define
class AgentConfigToolsDefinition:
    """The parts of an agent config definition that determine its effective tools. Other fields are ignored.

    Attributes:
        git_credentials (Union[Unset, AgentConfigDefinitionGitCredentials]): Integration whose git credentials the
            agent's machines use.
        interaction_handlers (Union['AgentConfigDefinitionInteractionHandlersType0', None, Unset]): Interaction handlers
            keyed by integration name.
        machine_sources (Union[None, Unset, list[Union['AgentConfigDefinitionMachineSourceType0',
            'AgentConfigDefinitionMachineSourceType1']]]):
        mcp (Union['AgentConfigDefinitionMCPServersType0', None, Unset]):
        memory_stores (Union[None, Unset, list['AgentConfigDefinitionMemoryStore']]):
        skills (Union[None, Unset, list[str]]):
        subagents (Union['AgentConfigDefinitionSubagentsType0', None, Unset]):
        tools (Union['AgentConfigDefinitionToolsType0', None, Unset]):
    """

    git_credentials: Union[Unset, "AgentConfigDefinitionGitCredentials"] = UNSET
    interaction_handlers: Union[
        "AgentConfigDefinitionInteractionHandlersType0", None, Unset
    ] = UNSET
    machine_sources: Union[
        None,
        Unset,
        list[
            Union[
                "AgentConfigDefinitionMachineSourceType0",
                "AgentConfigDefinitionMachineSourceType1",
            ]
        ],
    ] = UNSET
    mcp: Union["AgentConfigDefinitionMCPServersType0", None, Unset] = UNSET
    memory_stores: Union[None, Unset, list["AgentConfigDefinitionMemoryStore"]] = UNSET
    skills: Union[None, Unset, list[str]] = UNSET
    subagents: Union["AgentConfigDefinitionSubagentsType0", None, Unset] = UNSET
    tools: Union["AgentConfigDefinitionToolsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_config_definition_interaction_handlers_type_0 import (
            AgentConfigDefinitionInteractionHandlersType0,
        )
        from ..models.agent_config_definition_machine_source_type_0 import (
            AgentConfigDefinitionMachineSourceType0,
        )
        from ..models.agent_config_definition_mcp_servers_type_0 import (
            AgentConfigDefinitionMCPServersType0,
        )
        from ..models.agent_config_definition_subagents_type_0 import (
            AgentConfigDefinitionSubagentsType0,
        )
        from ..models.agent_config_definition_tools_type_0 import (
            AgentConfigDefinitionToolsType0,
        )

        git_credentials: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.git_credentials, Unset):
            git_credentials = self.git_credentials.to_dict()

        interaction_handlers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.interaction_handlers, Unset):
            interaction_handlers = UNSET
        elif isinstance(
            self.interaction_handlers, AgentConfigDefinitionInteractionHandlersType0
        ):
            interaction_handlers = self.interaction_handlers.to_dict()
        else:
            interaction_handlers = self.interaction_handlers

        machine_sources: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.machine_sources, Unset):
            machine_sources = UNSET
        elif isinstance(self.machine_sources, list):
            machine_sources = []
            for componentsschemas_agent_config_definition_machine_sources_type_0_item_data in self.machine_sources:
                componentsschemas_agent_config_definition_machine_sources_type_0_item: (
                    dict[str, Any]
                )
                if isinstance(
                    componentsschemas_agent_config_definition_machine_sources_type_0_item_data,
                    AgentConfigDefinitionMachineSourceType0,
                ):
                    componentsschemas_agent_config_definition_machine_sources_type_0_item = componentsschemas_agent_config_definition_machine_sources_type_0_item_data.to_dict()
                else:
                    componentsschemas_agent_config_definition_machine_sources_type_0_item = componentsschemas_agent_config_definition_machine_sources_type_0_item_data.to_dict()

                machine_sources.append(
                    componentsschemas_agent_config_definition_machine_sources_type_0_item
                )

        else:
            machine_sources = self.machine_sources

        mcp: Union[None, Unset, dict[str, Any]]
        if isinstance(self.mcp, Unset):
            mcp = UNSET
        elif isinstance(self.mcp, AgentConfigDefinitionMCPServersType0):
            mcp = self.mcp.to_dict()
        else:
            mcp = self.mcp

        memory_stores: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.memory_stores, Unset):
            memory_stores = UNSET
        elif isinstance(self.memory_stores, list):
            memory_stores = []
            for (
                componentsschemas_agent_config_definition_memory_stores_type_0_item_data
            ) in self.memory_stores:
                componentsschemas_agent_config_definition_memory_stores_type_0_item = componentsschemas_agent_config_definition_memory_stores_type_0_item_data.to_dict()
                memory_stores.append(
                    componentsschemas_agent_config_definition_memory_stores_type_0_item
                )

        else:
            memory_stores = self.memory_stores

        skills: Union[None, Unset, list[str]]
        if isinstance(self.skills, Unset):
            skills = UNSET
        elif isinstance(self.skills, list):
            skills = self.skills

        else:
            skills = self.skills

        subagents: Union[None, Unset, dict[str, Any]]
        if isinstance(self.subagents, Unset):
            subagents = UNSET
        elif isinstance(self.subagents, AgentConfigDefinitionSubagentsType0):
            subagents = self.subagents.to_dict()
        else:
            subagents = self.subagents

        tools: Union[None, Unset, dict[str, Any]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, AgentConfigDefinitionToolsType0):
            tools = self.tools.to_dict()
        else:
            tools = self.tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if git_credentials is not UNSET:
            field_dict["git_credentials"] = git_credentials
        if interaction_handlers is not UNSET:
            field_dict["interaction_handlers"] = interaction_handlers
        if machine_sources is not UNSET:
            field_dict["machine_sources"] = machine_sources
        if mcp is not UNSET:
            field_dict["mcp"] = mcp
        if memory_stores is not UNSET:
            field_dict["memory_stores"] = memory_stores
        if skills is not UNSET:
            field_dict["skills"] = skills
        if subagents is not UNSET:
            field_dict["subagents"] = subagents
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_git_credentials import (
            AgentConfigDefinitionGitCredentials,
        )
        from ..models.agent_config_definition_interaction_handlers_type_0 import (
            AgentConfigDefinitionInteractionHandlersType0,
        )
        from ..models.agent_config_definition_machine_source_type_0 import (
            AgentConfigDefinitionMachineSourceType0,
        )
        from ..models.agent_config_definition_machine_source_type_1 import (
            AgentConfigDefinitionMachineSourceType1,
        )
        from ..models.agent_config_definition_mcp_servers_type_0 import (
            AgentConfigDefinitionMCPServersType0,
        )
        from ..models.agent_config_definition_memory_store import (
            AgentConfigDefinitionMemoryStore,
        )
        from ..models.agent_config_definition_subagents_type_0 import (
            AgentConfigDefinitionSubagentsType0,
        )
        from ..models.agent_config_definition_tools_type_0 import (
            AgentConfigDefinitionToolsType0,
        )

        d = dict(src_dict)
        _git_credentials = d.pop("git_credentials", UNSET)
        git_credentials: Union[Unset, AgentConfigDefinitionGitCredentials]
        if isinstance(_git_credentials, Unset):
            git_credentials = UNSET
        else:
            git_credentials = AgentConfigDefinitionGitCredentials.from_dict(
                _git_credentials
            )

        def _parse_interaction_handlers(
            data: object,
        ) -> Union["AgentConfigDefinitionInteractionHandlersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_config_definition_interaction_handlers_type_0 = AgentConfigDefinitionInteractionHandlersType0.from_dict(
                    data
                )

                return componentsschemas_agent_config_definition_interaction_handlers_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union["AgentConfigDefinitionInteractionHandlersType0", None, Unset],
                data,
            )

        interaction_handlers = _parse_interaction_handlers(
            d.pop("interaction_handlers", UNSET)
        )

        def _parse_machine_sources(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[
                Union[
                    "AgentConfigDefinitionMachineSourceType0",
                    "AgentConfigDefinitionMachineSourceType1",
                ]
            ],
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_agent_config_definition_machine_sources_type_0 = []
                _componentsschemas_agent_config_definition_machine_sources_type_0 = data
                for componentsschemas_agent_config_definition_machine_sources_type_0_item_data in _componentsschemas_agent_config_definition_machine_sources_type_0:

                    def _parse_componentsschemas_agent_config_definition_machine_sources_type_0_item(
                        data: object,
                    ) -> Union[
                        "AgentConfigDefinitionMachineSourceType0",
                        "AgentConfigDefinitionMachineSourceType1",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemas_agent_config_definition_machine_source_type_0 = AgentConfigDefinitionMachineSourceType0.from_dict(
                                data
                            )

                            return componentsschemas_agent_config_definition_machine_source_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_agent_config_definition_machine_source_type_1 = AgentConfigDefinitionMachineSourceType1.from_dict(
                            data
                        )

                        return componentsschemas_agent_config_definition_machine_source_type_1

                    componentsschemas_agent_config_definition_machine_sources_type_0_item = _parse_componentsschemas_agent_config_definition_machine_sources_type_0_item(
                        componentsschemas_agent_config_definition_machine_sources_type_0_item_data
                    )

                    componentsschemas_agent_config_definition_machine_sources_type_0.append(
                        componentsschemas_agent_config_definition_machine_sources_type_0_item
                    )

                return componentsschemas_agent_config_definition_machine_sources_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[
                        Union[
                            "AgentConfigDefinitionMachineSourceType0",
                            "AgentConfigDefinitionMachineSourceType1",
                        ]
                    ],
                ],
                data,
            )

        machine_sources = _parse_machine_sources(d.pop("machine_sources", UNSET))

        def _parse_mcp(
            data: object,
        ) -> Union["AgentConfigDefinitionMCPServersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_config_definition_mcp_servers_type_0 = (
                    AgentConfigDefinitionMCPServersType0.from_dict(data)
                )

                return componentsschemas_agent_config_definition_mcp_servers_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union["AgentConfigDefinitionMCPServersType0", None, Unset], data
            )

        mcp = _parse_mcp(d.pop("mcp", UNSET))

        def _parse_memory_stores(
            data: object,
        ) -> Union[None, Unset, list["AgentConfigDefinitionMemoryStore"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_agent_config_definition_memory_stores_type_0 = []
                _componentsschemas_agent_config_definition_memory_stores_type_0 = data
                for componentsschemas_agent_config_definition_memory_stores_type_0_item_data in _componentsschemas_agent_config_definition_memory_stores_type_0:
                    componentsschemas_agent_config_definition_memory_stores_type_0_item = AgentConfigDefinitionMemoryStore.from_dict(
                        componentsschemas_agent_config_definition_memory_stores_type_0_item_data
                    )

                    componentsschemas_agent_config_definition_memory_stores_type_0.append(
                        componentsschemas_agent_config_definition_memory_stores_type_0_item
                    )

                return componentsschemas_agent_config_definition_memory_stores_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[None, Unset, list["AgentConfigDefinitionMemoryStore"]], data
            )

        memory_stores = _parse_memory_stores(d.pop("memory_stores", UNSET))

        def _parse_skills(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_agent_config_definition_skills_type_0 = cast(
                    list[str], data
                )

                return componentsschemas_agent_config_definition_skills_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        skills = _parse_skills(d.pop("skills", UNSET))

        def _parse_subagents(
            data: object,
        ) -> Union["AgentConfigDefinitionSubagentsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_config_definition_subagents_type_0 = (
                    AgentConfigDefinitionSubagentsType0.from_dict(data)
                )

                return componentsschemas_agent_config_definition_subagents_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentConfigDefinitionSubagentsType0", None, Unset], data)

        subagents = _parse_subagents(d.pop("subagents", UNSET))

        def _parse_tools(
            data: object,
        ) -> Union["AgentConfigDefinitionToolsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_config_definition_tools_type_0 = (
                    AgentConfigDefinitionToolsType0.from_dict(data)
                )

                return componentsschemas_agent_config_definition_tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentConfigDefinitionToolsType0", None, Unset], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        agent_config_tools_definition = cls(
            git_credentials=git_credentials,
            interaction_handlers=interaction_handlers,
            machine_sources=machine_sources,
            mcp=mcp,
            memory_stores=memory_stores,
            skills=skills,
            subagents=subagents,
            tools=tools,
        )

        agent_config_tools_definition.additional_properties = d
        return agent_config_tools_definition

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
