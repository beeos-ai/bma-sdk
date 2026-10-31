from typing import Literal, cast

MCPServerAuthRequiredErrorCode = Literal["unprocessable"]

MCP_SERVER_AUTH_REQUIRED_ERROR_CODE_VALUES: set[MCPServerAuthRequiredErrorCode] = {
    "unprocessable",
}


def check_mcp_server_auth_required_error_code(
    value: str,
) -> MCPServerAuthRequiredErrorCode:
    if value in MCP_SERVER_AUTH_REQUIRED_ERROR_CODE_VALUES:
        return cast(MCPServerAuthRequiredErrorCode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_REQUIRED_ERROR_CODE_VALUES!r}"
    )
