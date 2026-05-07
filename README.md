<div align="center">

# ⚡ FastMCP Template

**A production-ready template for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers with [FastMCP](https://github.com/jlowin/fastmcp).**

![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-3.0.1-blue.svg?style=for-the-badge)

</div>

---

## Features

- **[FastMCP](https://github.com/jlowin/fastmcp)** — Framework for building MCP servers
- **[uv](https://docs.astral.sh/uv/)** — Modern Python package and dependency manager
- **[ty](https://github.com/tjdevries/ty)** — Static type checker
- **[ruff](https://docs.astral.sh/ruff/)** — Fast Python linter & formatter
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Configuration management from environment variables
- **Testing with coverage** — pytest + pytest-asyncio with code coverage reports
- **Production-ready Dockerfile** — Multi-stage build with non-root user, bytecode compilation, and minimal base image
- **Copilot MCP integration** — Pre-configured `.vscode/mcp.json` for accessing FastMCP documentation via MCP

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

### 3. Run manually

```bash
uv run fastmcp run dev.fastmcp.json --reload
```

Run the production ASGI app locally:

```bash
MCP_ENV=production uv run uvicorn src.server:app --host 0.0.0.0 --port 8000
```

---

## Configuration

Settings are loaded from environment variables (prefix `MCP_`) or a `.env` file.

| Variable        | Default  | Description                                      |
|-----------------|----------|--------------------------------------------------|
| `MCP_SERVICE_NAME` | `MCP Server` | FastMCP service name                        |
| `MCP_ENV`       | `development` | Runtime mode (`development` or `production`) |

**Example `.env`:**

```env
MCP_SERVICE_NAME=My MCP Server
MCP_ENV=development
```

---

## Available Commands

| Command       | Description                                    |
|---------------|------------------------------------------------|
| `make dev`    | Run FastMCP in dev mode (`stdio`) with auto-reload |
| `make test`   | Run the test suite with coverage report        |
| `make build`  | Build the Docker image (`docker build -t mcp:latest .`) |
| `make start`  | Run the container in production (`docker run -p 8000:8000 mcp:latest`) |
---



## Adding Tools

Register new tools in [src/server.py](src/server.py):

```python
@mcp.tool
def my_tool(param: str) -> str:
    """Description shown to the LLM."""
    return param.upper()
```
