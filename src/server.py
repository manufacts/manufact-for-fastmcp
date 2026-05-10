"""Fastmcp fixture: minimal echo + widget tool exposed via streamable HTTP."""

from fastmcp import FastMCP
from mcp.types import EmbeddedResource, TextContent, TextResourceContents
from pydantic import AnyUrl
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import get_settings

settings = get_settings()

mcp = FastMCP(name=settings.service_name)


@mcp.tool
def echo(text: str) -> str:
    """Echo the input back as text."""
    return text


@mcp.tool
def greet_widget(name: str) -> list[TextContent | EmbeddedResource]:
    """Greet someone and return an HTML widget rendered by the MCP client."""
    html = (
        '<!doctype html><html><body style="font:16px/1.4 system-ui;padding:24px">'
        f'<h1 style="margin:0 0 8px">Hello, {name}!</h1>'
        '<p style="color:#555">Greeting widget served by mcp-detect-fastmcp.</p>'
        '</body></html>'
    )
    return [
        TextContent(type="text", text=f"Hello, {name}!"),
        EmbeddedResource(
            type="resource",
            resource=TextResourceContents(
                uri=AnyUrl(f"ui://greet/{name}"),
                mimeType="text/html",
                text=html,
            ),
        ),
    ]


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy"})


# Run in ASGI mode in production. Keep `app` defined unconditionally so
# `uvicorn src.server:app` works in any environment (cloud or local) — the
# config-driven `production` toggle is a relic of the original starter.
# `stateless_http=True` so each request handles its own MCP session (matches
# the streamable-HTTP fixtures used by the cloud post-deploy /mcp probe).
app = mcp.http_app(stateless_http=True)
