import pytest
from httpx import ASGITransport, AsyncClient
from starlette.authentication import AuthCredentials
from starlette.requests import Request
from starlette.types import Scope

from social_network_mcp.auth.api_key_validator import (
    ApiKeyAuthenticationBackend,
    ApiKeyTokenVerifier,
    build_token_verifier,
)
from social_network_mcp.config import McpServerConfig
from social_network_mcp.server import build_http_app


@pytest.fixture
def auth_config():
    return McpServerConfig(
        transport="streamable-http",
        host="127.0.0.1",
        port=8081,
        log_level="INFO",
        django_settings_module="social_network.settings.local",
        api_keys=frozenset({"test-api-key"}),
        require_auth=True,
        resource_server_url="http://127.0.0.1:8081/mcp",
        issuer_url="http://localhost",
    )


def _build_http_scope(headers: dict[str, str]) -> Scope:
    encoded_headers = [
        (key.lower().encode(), value.encode())
        for key, value in headers.items()
    ]
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/mcp",
        "raw_path": b"/mcp",
        "query_string": b"",
        "headers": encoded_headers,
        "client": ("127.0.0.1", 1234),
        "server": ("test", 80),
    }


@pytest.mark.asyncio
async def test_health_endpoint_is_public(auth_config):
    app = build_http_app(auth_config)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_mcp_endpoint_rejects_missing_api_key(auth_config):
    app = build_http_app(auth_config)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/mcp", json={})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_api_key_token_verifier_accepts_valid_key():
    verifier = ApiKeyTokenVerifier(api_keys=frozenset({"test-api-key"}))
    auth_info = await verifier.verify_token("test-api-key")

    assert auth_info is not None
    assert auth_info.client_id == "test-api"


@pytest.mark.asyncio
async def test_api_key_token_verifier_rejects_invalid_key():
    verifier = ApiKeyTokenVerifier(api_keys=frozenset({"test-api-key"}))
    auth_info = await verifier.verify_token("wrong-key")

    assert auth_info is None


@pytest.mark.asyncio
async def test_api_key_authentication_backend_accepts_bearer_header():
    backend = ApiKeyAuthenticationBackend(api_keys=frozenset({"test-api-key"}))
    scope = _build_http_scope({"Authorization": "Bearer test-api-key"})
    request = Request(scope)

    result = await backend.authenticate(request)

    assert result is not None
    credentials, user = result
    assert isinstance(credentials, AuthCredentials)
    assert user.is_authenticated


@pytest.mark.asyncio
async def test_api_key_authentication_backend_accepts_x_api_key_header():
    backend = ApiKeyAuthenticationBackend(api_keys=frozenset({"test-api-key"}))
    scope = _build_http_scope({"X-API-Key": "test-api-key"})
    request = Request(scope)

    result = await backend.authenticate(request)

    assert result is not None
    _, user = result
    assert user.is_authenticated


def test_build_token_verifier_returns_none_for_empty_keys():
    assert build_token_verifier(frozenset()) is None
