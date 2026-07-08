# Social Network MCP Server

Production-ready MCP server exposing `fb_post` operations to any MCP-compatible AI client.

## Tools

| Tool | Description |
|------|-------------|
| `create_post` | Create a post (`user_id`, `post_content`) |
| `get_post` | Get post details (`post_id`) |
| `create_comment` | Add a comment (`user_id`, `post_id`, `comment_content`) |
| `react_to_post` | Toggle reaction (`user_id`, `post_id`, `reaction_type`) |
| `delete_post` | Delete a post (`user_id`, `post_id`) |

## Local Development (stdio)

```bash
export DJANGO_SETTINGS_MODULE=social_network.settings.local
poetry run python -m social_network_mcp --transport stdio
```

Or use the included [`.cursor/mcp.json`](../.cursor/mcp.json) to connect from Cursor.

## Remote Clients (Streamable HTTP)

```bash
export DJANGO_SETTINGS_MODULE=social_network.settings.prod
export MCP_TRANSPORT=streamable-http
export MCP_HOST=0.0.0.0
export MCP_PORT=8081
export MCP_API_KEYS=client-a-key,client-b-key
export MCP_REQUIRE_AUTH=true

poetry run python -m social_network_mcp --transport streamable-http --host 0.0.0.0 --port 8081
```

Client configuration:

```json
{
  "mcpServers": {
    "social-network": {
      "url": "https://mcp.your-domain.com/mcp",
      "headers": {
        "Authorization": "Bearer your-api-key"
      }
    }
  }
}
```

`X-API-Key` is also supported:

```json
{
  "headers": {
    "X-API-Key": "your-api-key"
  }
}
```

## Production Deployment

1. Build and run the Docker image:

```bash
docker build -f Dockerfile.mcp -t social-network-mcp .
docker run -p 8081:8081 \
  -e DJANGO_SETTINGS_MODULE=social_network.settings.prod \
  -e MCP_API_KEYS=your-secret-key \
  -e MCP_REQUIRE_AUTH=true \
  social-network-mcp
```

2. Place behind a TLS-terminating reverse proxy (Nginx, ALB).
3. Health check: `GET /health` (no auth required).
4. Scale horizontally — the server is stateless (`stateless_http=True`).

### Nginx example

```nginx
location /mcp {
    proxy_pass http://mcp_backend;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
    proxy_read_timeout 300s;
}

location /health {
    proxy_pass http://mcp_backend;
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SETTINGS_MODULE` | `social_network.settings.local` | Django settings |
| `MCP_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `MCP_HOST` | `127.0.0.1` | HTTP bind host |
| `MCP_PORT` | `8081` | HTTP bind port |
| `MCP_API_KEYS` | _(empty)_ | Comma-separated API keys |
| `MCP_REQUIRE_AUTH` | `true` for HTTP, `false` for stdio | Require API key |
| `MCP_LOG_LEVEL` | `INFO` | Log level |

## Architecture

MCP tool handlers mirror `fb_post/views/*/api_wrapper.py` — they wire interactors and storage with MCP presenters that return structured dicts instead of HTTP responses. No business logic lives in the MCP layer.
