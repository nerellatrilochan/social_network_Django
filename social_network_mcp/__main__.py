import argparse
import logging
import os
import sys

from social_network_mcp.bootstrap import setup_django
from social_network_mcp.config import McpServerConfig
from social_network_mcp.server import build_http_app, create_mcp_server


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Social Network MCP server for fb_post operations",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default=os.environ.get("MCP_TRANSPORT", "stdio"),
        help="MCP transport protocol",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("MCP_HOST", "127.0.0.1"),
        help="Host for streamable-http transport",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("MCP_PORT", "8081")),
        help="Port for streamable-http transport",
    )
    parser.add_argument(
        "--log-level",
        default=os.environ.get("MCP_LOG_LEVEL", "INFO"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    os.environ["MCP_TRANSPORT"] = args.transport
    os.environ["MCP_HOST"] = args.host
    os.environ["MCP_PORT"] = str(args.port)
    os.environ["MCP_LOG_LEVEL"] = args.log_level

    config = McpServerConfig.from_env()
    _configure_logging(config.log_level)
    setup_django()

    if config.transport == "stdio":
        create_mcp_server(config).run(transport="stdio")
        return

    if config.transport == "streamable-http":
        import uvicorn

        app = build_http_app(config)
        uvicorn.run(
            app,
            host=config.host,
            port=config.port,
            log_level=config.log_level.lower(),
        )
        return

    raise ValueError(f"Unsupported transport: {config.transport}")


if __name__ == "__main__":
    main()
