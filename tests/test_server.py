"""Tests for server-level MCP operations."""

from fastmcp import Client


async def test_ping(mcp_client: Client):
    assert await mcp_client.ping() is True
