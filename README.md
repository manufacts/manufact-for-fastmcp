[![Deploy to mcp-use](https://cdn.mcp-use.com/deploy.svg)](https://mcp-use.com/deploy/start?repository-url=https%3A%2F%2Fgithub.com%2Fmanufacts%2Fmanufact-for-fastmcp&branch=main&project-name=manufact-for-fastmcp&port=8000&start-command=uvicorn+src.server%3Aapp+--host+0.0.0.0+--port+8000&runtime=python&base-image=python%3A3.12)

<div align="center">

# ⚡ FastMCP MCP Apps example

**Reference server for the [FastMCP deploy guide](https://mcp-use.com/blog/mcp-app-with-fastmcp)** — same `echo` + `greet_widget` example used in our [seven-framework comparison](https://mcp-use.com/blog/deploying-seven-mcp-frameworks).

![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-3.2.4+-blue.svg?style=for-the-badge)

**Live demo:** [`fast-zero-2g0gy.run.mcp-use.com/mcp`](https://fast-zero-2g0gy.run.mcp-use.com/mcp)

</div>

---

## Deploy to Manufact Cloud

Click the badge above, or open the [one-click deploy flow](https://mcp-use.com/deploy/start?repository-url=https%3A%2F%2Fgithub.com%2Fmanufacts%2Fmanufact-for-fastmcp&branch=main&project-name=manufact-for-fastmcp&port=8000&start-command=uvicorn+src.server%3Aapp+--host+0.0.0.0+--port+8000&runtime=python&base-image=python%3A3.12). Sign in, connect GitHub, and Manufact clones this repo into your account and deploys it.

If you deploy manually from the dashboard instead:

| Setting | Value |
| --- | --- |
| **Port** | `8000` |
| **Build command** | *(leave empty — Manufact runs `uv sync --frozen` when `uv.lock` is present, otherwise `pip install .`)* |
| **Start command** | `uvicorn src.server:app --host 0.0.0.0 --port 8000` |

Manufact reads `requires-python` from `pyproject.toml` and picks a matching Python base image (3.11, 3.12, or 3.13). Keep `pyproject.toml` and `uv.lock` in sync — run `uv lock` after dependency changes and commit both files.

---

## What's in this repo

- An `echo` tool (text-only)
- A `greet_widget` tool with `app=True` that returns a [Prefab UI](https://github.com/jlowin/fastmcp) MCP App view
- Streamable HTTP at `/mcp` via uvicorn + FastMCP ASGI app

---

## Features

- **[FastMCP](https://github.com/jlowin/fastmcp)** with the `[apps]` extra — Prefab UI widgets without a frontend build
- **[uv](https://docs.astral.sh/uv/)** — dependency management and lockfile
- **[ty](https://github.com/tjdevries/ty)** — static type checker
- **[ruff](https://docs.astral.sh/ruff/)** — linter and formatter
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — configuration from environment variables
- **Testing with coverage** — pytest + pytest-asyncio
- **Production Dockerfile** — multi-stage build with non-root user

---

## Requirements

- [uv](https://docs.astral.sh/uv/) (package manager)

---

## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Run the server (development)

```bash
make dev
```

This runs FastMCP with `dev.fastmcp.json` in `stdio` transport mode and auto-reload.

### 3. Run the production HTTP server locally

```bash
MCP_ENV=production uv run uvicorn src.server:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/mcp`.

### 4. Run manually (stdio)

```bash
uv run fastmcp run dev.fastmcp.json --reload
```

---

## Configuration

Settings are loaded from environment variables (prefix `MCP_`) or a `.env` file.

| Variable | Default | Description |
| --- | --- | --- |
| `MCP_SERVICE_NAME` | `MCP Server` | FastMCP service name |
| `MCP_ENV` | `development` | Runtime mode (`development` or `production`) |

**Example `.env`:**

```env
MCP_SERVICE_NAME=My MCP Server
MCP_ENV=development
```

---

## Available Commands

| Command | Description |
| --- | --- |
| `make dev` | Run FastMCP in dev mode (`stdio`) with auto-reload |
| `make test` | Run the test suite with coverage report |
| `make build` | Build the Docker image (`docker build -t mcp:latest .`) |
| `make start` | Run the container in production (`docker run -p 8000:8000 mcp:latest`) |

---

## Adding Tools

Register new tools in [src/server.py](src/server.py):

```python
@mcp.tool
def my_tool(param: str) -> str:
    """Description shown to the LLM."""
    return param.upper()
```

For MCP App widgets, use `@mcp.tool(app=True)` and return a `PrefabApp` — see `greet_widget` in the same file.
