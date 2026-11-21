import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("extensions_input", Path(__file__).resolve().parent / "extensions_input.py")
extensions_input = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extensions_input)


def public_contract():
    ok = {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Machine"}}}}}
    return {
        "openapi": "3.1.0",
        "info": {"title": "BMA", "version": "1"},
        "servers": [{"url": "https://api.example"}],
        "paths": {
            "/v1/agents": {"get": {"operationId": "listAgents", "x-bma-extension": False, "responses": {"200": {}}}},
            "/v1/machines/{machine_id}": {
                "parameters": [{"$ref": "#/components/parameters/MachineID"}],
                "get": {"operationId": "getMachine", "x-bma-extension": True, "responses": ok},
            },
            "/v1/machines/{machine_id}/backups": {
                "get": {
                    "operationId": "listMachineBackups",
                    "x-bma-extension": True,
                    "responses": {"200": {"content": {"application/json": {"schema": {"type": "object"}}}}},
                },
            },
        },
        "components": {
            "securitySchemes": {"key": {"type": "apiKey", "in": "header", "name": "x-api-key"}},
            "parameters": {"MachineID": {"name": "machine_id", "in": "path", "required": True, "schema": {"type": "string"}}},
            "responses": {},
            "schemas": {
                "Agent": {"type": "object"},
                "Machine": {"type": "object", "properties": {"pool": {"$ref": "#/components/schemas/Pool"}}},
                "Pool": {"type": "object"},
            },
        },
    }


def test_keeps_extension_operations_under_the_v1_server_and_their_schemas():
    doc = extensions_input.extensions(public_contract())
    assert doc["servers"] == [{"url": "/v1"}]
    assert list(doc["paths"]) == ["/machines/{machine_id}", "/machines/{machine_id}/backups"]
    assert doc["paths"]["/machines/{machine_id}"]["parameters"] == [{"$ref": "#/components/parameters/MachineID"}]
    assert list(doc["components"]["parameters"]) == ["MachineID"]
    assert list(doc["components"]["schemas"]) == ["Machine", "Pool", "ListMachineBackupsResponse"]


def test_inline_bodies_become_named_components():
    doc = extensions_input.extensions(public_contract())
    media = doc["paths"]["/machines/{machine_id}/backups"]["get"]["responses"]["200"]["content"]["application/json"]
    assert media["schema"] == {"$ref": "#/components/schemas/ListMachineBackupsResponse"}


def test_extension_outside_v1_is_rejected():
    doc = public_contract()
    doc["paths"]["/other"] = {"get": {"operationId": "other", "x-bma-extension": True, "responses": {}}}
    with pytest.raises(SystemExit):
        extensions_input.extensions(doc)
