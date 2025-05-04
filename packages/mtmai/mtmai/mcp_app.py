from fastmcp import FastMCP

from mtmai.core.config import settings

mcpApp = FastMCP(
    name="My MCP Server",
    on_duplicate_tools="error",  # Set duplicate handling
    on_duplicate_resources="error",
    on_duplicate_prompts="error",
    log_level="DEBUG",
    port=settings.PORT,
)


@mcpApp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"
    return f"Hello, {name}!"
