"""Fastmcp fixture: echo tool + Prefab UI greet widget.

Follows the recommended FastMCP Apps pattern:
- ``@mcp.tool(app=True)`` returning a ``PrefabApp`` for the widget tool
- Plain ``@mcp.tool`` for the text-only echo tool

See https://gofastmcp.com/apps/prefab for the full pattern.
"""

from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Card, CardContent, Column, Heading, Muted
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import get_settings

settings = get_settings()

mcp = FastMCP(
    name=settings.service_name,
    instructions="Smoke-test fixture for FastMCP framework detection (MCP Apps).",
)


@mcp.tool
def echo(text: str) -> str:
    """Echo the input back as text."""
    return text


@mcp.tool(app=True)
def greet_widget(name: str) -> PrefabApp:
    """Greet someone and render a Prefab UI greeting card.

    Renders an interactive UI in MCP Apps-capable hosts (ChatGPT, Claude, etc.)
    via FastMCP's Prefab UI integration.
    """
    with Column(gap=4, css_class="p-6") as view:
        with Card():
            with CardContent():
                Heading(f"Hello, {name}!")
                Muted("Greeting widget served by mcp-detect-fastmcp.")

    return PrefabApp(view=view)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy"})


# Streamable-HTTP ASGI app (mounted at /mcp by FastMCP). `stateless_http=True`
# so each request handles its own MCP session (matches the post-deploy probe).
app = mcp.http_app(stateless_http=True)
