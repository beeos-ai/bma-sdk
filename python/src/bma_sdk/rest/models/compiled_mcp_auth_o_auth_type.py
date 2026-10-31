from typing import Literal, cast

CompiledMCPAuthOAuthType = Literal["oauth"]

COMPILED_MCP_AUTH_O_AUTH_TYPE_VALUES: set[CompiledMCPAuthOAuthType] = {
    "oauth",
}


def check_compiled_mcp_auth_o_auth_type(value: str) -> CompiledMCPAuthOAuthType:
    if value in COMPILED_MCP_AUTH_O_AUTH_TYPE_VALUES:
        return cast(CompiledMCPAuthOAuthType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_MCP_AUTH_O_AUTH_TYPE_VALUES!r}"
    )
