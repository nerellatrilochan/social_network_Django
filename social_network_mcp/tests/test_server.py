import pytest

from social_network_mcp.config import McpServerConfig
from social_network_mcp.server import create_mcp_server


def test_create_mcp_server_registers_all_tools():
    config = McpServerConfig(
        transport="stdio",
        host="127.0.0.1",
        port=8081,
        log_level="INFO",
        django_settings_module="social_network.settings.local",
        api_keys=frozenset(),
        require_auth=False,
        resource_server_url="http://127.0.0.1:8081/mcp",
        issuer_url="http://localhost",
    )
    mcp = create_mcp_server(config)

    import asyncio

    tools = asyncio.run(mcp.list_tools())
    tool_names = {tool.name for tool in tools}

    assert tool_names == {
        "create_post",
        "get_post",
        "create_comment",
        "react_to_post",
        "delete_post",
    }


def test_build_http_app_requires_api_keys_when_auth_enabled():
    config = McpServerConfig(
        transport="streamable-http",
        host="127.0.0.1",
        port=8081,
        log_level="INFO",
        django_settings_module="social_network.settings.local",
        api_keys=frozenset(),
        require_auth=True,
        resource_server_url="http://127.0.0.1:8081/mcp",
        issuer_url="http://localhost",
    )

    from social_network_mcp.server import build_http_app

    with pytest.raises(ValueError, match="MCP_API_KEYS is empty"):
        build_http_app(config)
