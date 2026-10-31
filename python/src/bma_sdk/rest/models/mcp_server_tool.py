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
    from ..models.mcp_server_tool_annotations import MCPServerToolAnnotations
    from ..models.mcp_server_tool_input_schema import MCPServerToolInputSchema
    from ..models.mcp_server_tool_output_schema import MCPServerToolOutputSchema


T = TypeVar("T", bound="MCPServerTool")


@_attrs_define
class MCPServerTool:
    """
    Attributes:
        name (str): Tool name as advertised by the server. Referenced from agent config
            `mcp_servers.<key>.tools.<name>`.
        input_schema (MCPServerToolInputSchema): JSON Schema for the tool's arguments.
        title (Union[Unset, str]):
        description (Union[Unset, str]):
        output_schema (Union[Unset, MCPServerToolOutputSchema]): JSON Schema for the tool's structured result, when the
            server advertises one.
        annotations (Union[Unset, MCPServerToolAnnotations]):
    """

    name: str
    input_schema: "MCPServerToolInputSchema"
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    output_schema: Union[Unset, "MCPServerToolOutputSchema"] = UNSET
    annotations: Union[Unset, "MCPServerToolAnnotations"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        input_schema = self.input_schema.to_dict()

        title = self.title

        description = self.description

        output_schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.output_schema, Unset):
            output_schema = self.output_schema.to_dict()

        annotations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "input_schema": input_schema,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema
        if annotations is not UNSET:
            field_dict["annotations"] = annotations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_server_tool_annotations import MCPServerToolAnnotations
        from ..models.mcp_server_tool_input_schema import MCPServerToolInputSchema
        from ..models.mcp_server_tool_output_schema import MCPServerToolOutputSchema

        d = dict(src_dict)
        name = d.pop("name")

        input_schema = MCPServerToolInputSchema.from_dict(d.pop("input_schema"))

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _output_schema = d.pop("output_schema", UNSET)
        output_schema: Union[Unset, MCPServerToolOutputSchema]
        if isinstance(_output_schema, Unset):
            output_schema = UNSET
        else:
            output_schema = MCPServerToolOutputSchema.from_dict(_output_schema)

        _annotations = d.pop("annotations", UNSET)
        annotations: Union[Unset, MCPServerToolAnnotations]
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = MCPServerToolAnnotations.from_dict(_annotations)

        mcp_server_tool = cls(
            name=name,
            input_schema=input_schema,
            title=title,
            description=description,
            output_schema=output_schema,
            annotations=annotations,
        )

        return mcp_server_tool
