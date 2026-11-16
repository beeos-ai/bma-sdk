import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "bundle_contract", Path(__file__).resolve().parents[1] / "bundle_contract.py"
)
bundle_contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle_contract)


def test_external_subschema_pointer_becomes_a_typed_component():
    extension = {
        "info": {},
        "paths": {
            "/machines": {
                "post": {
                    "schema": {"$ref": "openapi.yaml#/components/schemas/Machine/properties/harnesses"}
                }
            }
        },
        "components": {"schemas": {"Machine": {"type": "object"}}},
    }
    native = {
        "components": {
            "schemas": {
                "Machine": {"properties": {"harnesses": {"$ref": "#/components/schemas/Harnesses"}}},
                "Harnesses": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
    result = bundle_contract.bundle(extension, native)
    assert result["paths"]["/machines"]["post"]["schema"]["$ref"] == (
        "#/components/schemas/Machine_properties_harnesses"
    )
    assert result["components"]["schemas"]["Machine_properties_harnesses"] == {
        "$ref": "#/components/schemas/Harnesses"
    }
    assert result["components"]["schemas"]["Machine"] == extension["components"]["schemas"]["Machine"]
    assert result["components"]["schemas"]["Harnesses"] == native["components"]["schemas"]["Harnesses"]


def test_transitive_native_subschema_pointer_becomes_a_typed_component():
    extension = {
        "info": {},
        "paths": {"/machines": {"get": {"schema": {"$ref": "openapi.yaml#/components/schemas/Machine"}}}},
        "components": {"schemas": {}},
    }
    native = {
        "components": {
            "schemas": {
                "Machine": {"properties": {"harnesses": {"$ref": "#/components/schemas/Capabilities/properties/harnesses"}}},
                "Capabilities": {"properties": {"harnesses": {"type": "array", "items": {"type": "string"}}}},
            }
        }
    }
    result = bundle_contract.bundle(extension, native)
    assert result["components"]["schemas"]["Machine"]["properties"]["harnesses"] == {
        "$ref": "#/components/schemas/Capabilities_properties_harnesses"
    }
    assert result["components"]["schemas"]["Capabilities_properties_harnesses"] == {
        "type": "array", "items": {"type": "string"}
    }


def test_native_subschema_keeps_extension_name_distinct():
    extension = {
        "info": {},
        "paths": {"/machines": {"get": {"schema": {"$ref": "openapi.yaml#/components/schemas/Machine/properties/harnesses"}}}},
        "components": {"schemas": {"Machine_properties_harnesses": {"type": "boolean"}}},
    }
    native = {"components": {"schemas": {"Machine": {"properties": {"harnesses": {"type": "string"}}}}}}
    result = bundle_contract.bundle(extension, native)
    assert result["paths"]["/machines"]["get"]["schema"]["$ref"] == "#/components/schemas/NativeMachine_properties_harnesses"
    assert result["components"]["schemas"]["Machine_properties_harnesses"] == {"type": "boolean"}
    assert result["components"]["schemas"]["NativeMachine_properties_harnesses"] == {"type": "string"}


def test_native_subschema_name_collision_is_rejected():
    extension = {
        "info": {},
        "paths": {"/machines": {"get": {"schema": {"$ref": "openapi.yaml#/components/schemas/Machine/properties/harnesses"}}}},
        "components": {"schemas": {}},
    }
    native = {"components": {"schemas": {
        "Machine": {"properties": {"harnesses": {"$ref": "#/components/schemas/Machine_properties_harnesses"}}},
        "Machine_properties_harnesses": {"type": "string"},
    }}}
    with pytest.raises(ValueError, match="native schema references collide at Machine_properties_harnesses"):
        bundle_contract.bundle(extension, native)


def test_prefixed_native_name_does_not_overwrite_an_extension_schema():
    extension = {
        "info": {},
        "paths": {"/machines": {"get": {"schema": {"$ref": "openapi.yaml#/components/schemas/Machine"}}}},
        "components": {"schemas": {"Machine": {"type": "object"}, "NativeMachine": {"type": "boolean"}}},
    }
    native = {"components": {"schemas": {"Machine": {"type": "string"}}}}
    with pytest.raises(ValueError, match="native schema references collide at NativeMachine"):
        bundle_contract.bundle(extension, native)
