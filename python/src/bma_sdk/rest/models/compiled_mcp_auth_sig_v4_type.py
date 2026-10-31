from typing import Literal, cast

CompiledMCPAuthSigV4Type = Literal["sigv4"]

COMPILED_MCP_AUTH_SIG_V4_TYPE_VALUES: set[CompiledMCPAuthSigV4Type] = {
    "sigv4",
}


def check_compiled_mcp_auth_sig_v4_type(value: str) -> CompiledMCPAuthSigV4Type:
    if value in COMPILED_MCP_AUTH_SIG_V4_TYPE_VALUES:
        return cast(CompiledMCPAuthSigV4Type, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_MCP_AUTH_SIG_V4_TYPE_VALUES!r}"
    )
