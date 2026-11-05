"""Tests for the resource-map coverage rules of tools/sdkgen/sdkgen.py.

Run: uv run --no-project --with pyyaml --with pytest pytest -q tools/sdkgen
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent))
import sdkgen  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

DOC = {
    "openapi": "3.1.2",
    "paths": {
        "/orgs/{orgID}/projects/{projectID}/agents": {
            "parameters": [
                {"name": "orgID", "in": "path", "required": True},
                {"name": "projectID", "in": "path", "required": True},
            ],
            "get": {
                "operationId": "listAgents",
                "parameters": [{"name": "cursor", "in": "query"}, {"name": "limit", "in": "query"}],
                "responses": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Page"}}}}},
            },
            "post": {
                "operationId": "createAgent",
                "parameters": [{"name": "Idempotency-Key", "in": "header"}],
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object", "required": ["name"]}}}},
                "responses": {"201": {"content": {"application/json": {"schema": {"type": "object"}}}}},
            },
        },
        "/daemon/bootstrap": {"post": {"operationId": "bootstrapDaemon", "responses": {"204": {}}}},
    },
    "components": {
        "schemas": {
            "Page": {
                "type": "object",
                "properties": {"data": {"type": "array"}, "next_cursor": {"type": "string"}},
            }
        }
    },
}


def tree(section):
    contract = sdkgen.Contract(DOC, {})
    ops = contract.operations()
    return sdkgen.build_tree(section, ops), ops


def test_full_coverage_with_internal():
    (roots, used), ops = tree({
        "resources": {"agents": {"methods": {"list": "listAgents", "create": "createAgent"}}},
        "internal": ["bootstrapDaemon"],
    })
    assert used == {"listAgents", "createAgent"}
    assert ops["listAgents"].paginated
    assert ops["createAgent"].idempotency
    assert not ops["createAgent"].paginated
    assert [p.name for p in roots[0].methods[0].positional] == []


def test_unmapped_operation_fails():
    with pytest.raises(sdkgen.GenError, match="not mapped.*bootstrapDaemon"):
        tree({"resources": {"agents": {"methods": {"list": "listAgents", "create": "createAgent"}}}})


def test_duplicate_mapping_fails():
    with pytest.raises(sdkgen.GenError, match="mapped twice"):
        tree({
            "resources": {
                "agents": {"methods": {"list": "listAgents", "create": "createAgent", "again": "listAgents"}}
            },
            "internal": ["bootstrapDaemon"],
        })


def test_unknown_operation_fails():
    with pytest.raises(sdkgen.GenError, match="unknown operation nope"):
        tree({"resources": {"agents": {"methods": {"x": "nope"}}}})


def test_positional_scope_parameter():
    (roots, _), _ = tree({
        "resources": {
            "agents": {
                "methods": {
                    "list": {"operation": "listAgents", "positional": ["projectID"]},
                    "create": "createAgent",
                }
            }
        },
        "internal": ["bootstrapDaemon"],
    })
    assert [p.name for p in roots[0].methods[0].positional] == ["projectID"]


@pytest.mark.parametrize("section,contract", [
    ("rest", "contracts/bma/rest.openapi.yaml"),
    ("facade", "contracts/bma/facade-extensions.openapi.yaml"),
])
def test_repository_map_covers_contract(section, contract):
    config = yaml.safe_load((ROOT / "contracts/bma/sdk.resources.yaml").read_text())
    c = sdkgen.Contract(yaml.safe_load((ROOT / contract).read_text()), config["header_params"])
    ops = c.operations()
    _, used = sdkgen.build_tree(config[section], ops)
    assert used | set(config[section].get("internal") or []) == set(ops)
    if section == "rest":
        assert len(ops) == 244
        assert sum(op.paginated for op in ops.values()) == 39


# --- Python template (pygen) ---------------------------------------------------

import pygen  # noqa: E402

TYPES_DOC = {
    "components": {
        "schemas": {
            "Code": {"type": "string", "enum": ["a", "b"], "x-extensible-enum": True},
            "Flag": {"const": False},
            "When": {"type": "string", "format": "date-time"},
            "Block": {
                "type": "object",
                "required": ["type"],
                "properties": {"type": {"type": "string", "enum": ["text"]}, "meta": {"type": "object", "properties": {"k": {"type": "string"}}}},
            },
            "Blocks": {
                "oneOf": [{"$ref": "#/components/schemas/Block"}],
                "discriminator": {"propertyName": "type"},
            },
            "Nullable": {"type": ["integer", "null"]},
        }
    }
}


def test_pygen_model_and_param_types():
    models = pygen.Types(TYPES_DOC, "model")
    params = pygen.Types(TYPES_DOC, "param")
    for name in TYPES_DOC["components"]["schemas"]:
        models.schema_type(name)
        if not params.plain(name):
            params.schema_type(name)
    assert models.aliases["Code"] == 'Union[Literal["a", "b"], str]'
    assert models.aliases["Flag"] == "Literal[False]"
    assert models.aliases["When"] == "datetime"
    assert params.aliases["WhenParam"] == "Union[str, datetime]"
    assert models.aliases["Nullable"] == "Optional[int]"
    assert [f.name for f in models.classes["Block"].fields] == ["type", "meta"]
    assert "BlockMeta" in models.classes and "BlockMetaParam" in params.classes
    assert params.plain("Code") and not params.plain("Block")


def test_pygen_snake_names():
    assert pygen.snake("createGitHubSetup") == "create_github_setup"
    assert pygen.snake("startMcpOAuth") == "start_mcp_oauth"
    assert pygen.snake("toolCallID") == "tool_call_id"
    assert pygen.snake("connectBYOMachine") == "connect_byo_machine"


@pytest.mark.parametrize("section,contract", [
    ("rest", "contracts/bma/rest.openapi.yaml"),
    ("facade", "contracts/bma/facade-extensions.openapi.yaml"),
])
def test_pygen_repository_contract_compiles(section, contract, tmp_path):
    config = yaml.safe_load((ROOT / "contracts/bma/sdk.resources.yaml").read_text())
    c = sdkgen.Contract(yaml.safe_load((ROOT / contract).read_text()), config["header_params"])
    roots, used = sdkgen.build_tree(config[section], c.operations())
    assert sdkgen.write_python(c, roots, section, section.title(), tmp_path, len(used)) == 0
    for name in ("models.py", "params.py", "operations.py", "resources.py"):
        compile((tmp_path / name).read_text(), name, "exec")


# --- Go template (gogen) ------------------------------------------------------

import gogen  # noqa: E402


def test_gogen_names():
    assert gogen.go_name("apiKeys") == "APIKeys"
    assert gogen.go_name("mcpServers") == "MCPServers"
    assert gogen.singular("toolCalls") == "ToolCall"
    assert gogen.singular("memoryStores") == "MemoryStore"
    assert gogen.singular("me") == "Me"
    assert gogen.method_name("create") == "New" and gogen.method_name("retrieve") == "Get"
    assert gogen.method_name("startMcpOAuth") == "StartMCPOAuth"
    assert gogen.arg_name("agentID") == "agentID" and gogen.arg_name("session_id") == "sessionID"
