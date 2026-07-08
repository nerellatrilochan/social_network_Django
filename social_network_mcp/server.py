import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from social_network_mcp.adapters.tool_result_adapter import to_tool_result
from social_network_mcp.auth.api_key_validator import ApiKeyAuthenticationBackend
from social_network_mcp.config import McpServerConfig
from social_network_mcp.tools.create_comment_tool import handle_create_comment
from social_network_mcp.tools.create_post_tool import handle_create_post
from social_network_mcp.tools.delete_post_tool import handle_delete_post
from social_network_mcp.tools.get_post_tool import handle_get_post
from social_network_mcp.tools.react_to_post_tool import handle_react_to_post

logger = logging.getLogger(__name__)

REACTION_TYPES = Literal[
    "WOW",
    "LIT",
    "LOVE",
    "HAHA",
    "THUMBS-UP",
    "THUMBS-DOWN",
    "ANGRY",
    "SAD",
]


class RequireApiKeyMiddleware:
    """Reject unauthenticated requests to protected MCP routes."""

    def __init__(self, app, public_paths: frozenset[str]):
        self.app = app
        self.public_paths = public_paths

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if path in self.public_paths:
            await self.app(scope, receive, send)
            return

        user = scope.get("user")
        if user is None or not user.is_authenticated:
            response = JSONResponse(
                {"error": "Unauthorized", "message": "Valid API key required"},
                status_code=401,
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)


def _log_tool_call(tool_name: str) -> Callable:
    def decorator(handler: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
        @wraps(handler)
        def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
            started_at = time.perf_counter()
            try:
                result = to_tool_result(handler(*args, **kwargs))
            except Exception:
                logger.exception(
                    "mcp_tool_failed",
                    extra={"tool_name": tool_name},
                )
                raise

            duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
            logger.info(
                "mcp_tool_completed",
                extra={
                    "tool_name": tool_name,
                    "duration_ms": duration_ms,
                    "ok": result.get("ok"),
                    "status": result.get("status"),
                },
            )
            return result

        return wrapper

    return decorator


def create_mcp_server(config: McpServerConfig) -> FastMCP:
    mcp = FastMCP(
        "social-network-fb-post",
        instructions=(
            "MCP tools for the social network fb_post app. "
            "Use create_post, get_post, create_comment, react_to_post, "
            "and delete_post."
        ),
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        stateless_http=True,
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> Response:
        return JSONResponse({"status": "healthy", "service": "social-network-mcp"})

    @_log_tool_call("create_post")
    @mcp.tool(
        name="create_post",
        description="Create a new post for a user.",
    )
    def create_post(user_id: int, post_content: str) -> dict[str, Any]:
        return handle_create_post(user_id=user_id, post_content=post_content)

    @_log_tool_call("get_post")
    @mcp.tool(
        name="get_post",
        description="Get full post details including comments and reactions.",
    )
    def get_post(post_id: int) -> dict[str, Any]:
        return handle_get_post(post_id=post_id)

    @_log_tool_call("create_comment")
    @mcp.tool(
        name="create_comment",
        description="Create a comment on a post.",
    )
    def create_comment(
        user_id: int,
        post_id: int,
        comment_content: str,
    ) -> dict[str, Any]:
        return handle_create_comment(
            user_id=user_id,
            post_id=post_id,
            comment_content=comment_content,
        )

    @_log_tool_call("react_to_post")
    @mcp.tool(
        name="react_to_post",
        description="Toggle a reaction on a post.",
    )
    def react_to_post(
        user_id: int,
        post_id: int,
        reaction_type: REACTION_TYPES,
    ) -> dict[str, Any]:
        return handle_react_to_post(
            user_id=user_id,
            post_id=post_id,
            reaction_type=reaction_type,
        )

    @_log_tool_call("delete_post")
    @mcp.tool(
        name="delete_post",
        description="Delete a post. Only the post creator can delete it.",
    )
    def delete_post(user_id: int, post_id: int) -> dict[str, Any]:
        return handle_delete_post(user_id=user_id, post_id=post_id)

    return mcp


def build_http_app(config: McpServerConfig) -> Starlette:
    """Build the Streamable HTTP Starlette app with API key auth."""
    if config.require_auth and not config.api_keys:
        raise ValueError(
            "MCP_REQUIRE_AUTH is enabled but MCP_API_KEYS is empty",
        )

    mcp = create_mcp_server(config)
    base_app = mcp.streamable_http_app()

    if not config.require_auth:
        return base_app

    middleware = [
        Middleware(
            AuthenticationMiddleware,
            backend=ApiKeyAuthenticationBackend(config.api_keys),
        ),
        Middleware(
            RequireApiKeyMiddleware,
            public_paths=frozenset({"/health"}),
        ),
    ]

    return Starlette(
        debug=base_app.debug,
        routes=base_app.routes,
        middleware=middleware,
    )
