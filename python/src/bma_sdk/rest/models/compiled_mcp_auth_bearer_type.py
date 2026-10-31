from typing import Literal, cast

CompiledMCPAuthBearerType = Literal["bearer"]

COMPILED_MCP_AUTH_BEARER_TYPE_VALUES: set[CompiledMCPAuthBearerType] = {
    "bearer",
}


def check_compiled_mcp_auth_bearer_type(value: str) -> CompiledMCPAuthBearerType:
    if value in COMPILED_MCP_AUTH_BEARER_TYPE_VALUES:
        return cast(CompiledMCPAuthBearerType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_MCP_AUTH_BEARER_TYPE_VALUES!r}"
    )
