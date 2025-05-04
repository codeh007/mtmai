from fastmcp import FastMCP
from mtmai.core.config import settings

mcpApp = FastMCP(
    name="Mtmai MCP Server",
    on_duplicate_tools="error",
    on_duplicate_resources="error",
    on_duplicate_prompts="error",
    log_level="DEBUG",
    port=settings.PORT,
)


def setup_tools():
    from .tool_greet import greet  # noqa: F401


setup_tools()
