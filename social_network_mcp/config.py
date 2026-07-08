import os
from dataclasses import dataclass


@dataclass(frozen=True)
class McpServerConfig:
    transport: str
    host: str
    port: int
    log_level: str
    django_settings_module: str
    api_keys: frozenset[str]
    require_auth: bool
    resource_server_url: str
    issuer_url: str

    @classmethod
    def from_env(cls) -> "McpServerConfig":
        api_keys_raw = os.environ.get("MCP_API_KEYS", "")
        api_keys = frozenset(
            key.strip()
            for key in api_keys_raw.split(",")
            if key.strip()
        )
        transport = os.environ.get("MCP_TRANSPORT", "stdio")
        require_auth = os.environ.get(
            "MCP_REQUIRE_AUTH",
            "true" if transport == "streamable-http" else "false",
        ).lower() in {"1", "true", "yes"}

        return cls(
            transport=transport,
            host=os.environ.get("MCP_HOST", "127.0.0.1"),
            port=int(os.environ.get("MCP_PORT", "8081")),
            log_level=os.environ.get("MCP_LOG_LEVEL", "INFO").upper(),
            django_settings_module=os.environ.get(
                "DJANGO_SETTINGS_MODULE",
                "social_network.settings.local",
            ),
            api_keys=api_keys,
            require_auth=require_auth,
            resource_server_url=os.environ.get(
                "MCP_RESOURCE_SERVER_URL",
                f"http://{os.environ.get('MCP_HOST', '127.0.0.1')}:"
                f"{os.environ.get('MCP_PORT', '8081')}/mcp",
            ),
            issuer_url=os.environ.get(
                "MCP_ISSUER_URL",
                "http://localhost",
            ),
        )
