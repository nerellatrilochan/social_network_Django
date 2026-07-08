from mcp.server.auth.middleware.bearer_auth import AuthenticatedUser
from mcp.server.auth.provider import AccessToken, TokenVerifier
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection


class ApiKeyTokenVerifier:
    """Validate bearer tokens against configured API keys."""

    def __init__(self, api_keys: frozenset[str]):
        self._api_keys = api_keys

    async def verify_token(self, token: str) -> AccessToken | None:
        if not token or token not in self._api_keys:
            return None

        return AccessToken(
            token=token,
            client_id=token[:8],
            scopes=[],
            expires_at=None,
            subject=None,
            claims={"auth_type": "api_key"},
        )


class ApiKeyAuthenticationBackend(AuthenticationBackend):
    """Authenticate requests using Bearer tokens or X-API-Key headers."""

    def __init__(self, api_keys: frozenset[str]):
        self._api_keys = api_keys
        self._token_verifier = build_token_verifier(api_keys)

    async def authenticate(self, conn: HTTPConnection):
        token = self._extract_token(conn)
        if not token or not self._token_verifier:
            return None

        auth_info = await self._token_verifier.verify_token(token)
        if not auth_info:
            return None

        return AuthCredentials(auth_info.scopes), AuthenticatedUser(auth_info)

    @staticmethod
    def _extract_token(conn: HTTPConnection) -> str | None:
        auth_header = conn.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            return auth_header[7:].strip()

        api_key = conn.headers.get("x-api-key")
        if api_key:
            return api_key.strip()

        return None


def build_token_verifier(api_keys: frozenset[str]) -> TokenVerifier | None:
    if not api_keys:
        return None

    return ApiKeyTokenVerifier(api_keys=api_keys)
