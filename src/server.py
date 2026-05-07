from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import get_settings

settings = get_settings()

mcp = FastMCP(name=settings.service_name)


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy"})


# Run in ASGI mode in production
if settings.env == "production":
    app = mcp.http_app()
