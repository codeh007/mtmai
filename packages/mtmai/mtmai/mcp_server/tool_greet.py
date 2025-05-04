from loguru import logger

from .mcp_app import mcpApp


@mcpApp.tool()
def greet(name: str) -> str:
    """
    向用户问候
    """
    logger.info(f"Greeting {name}")
    return f"Hello, {name}!"


@mcpApp.tool()
def search_file(name: str) -> str:
    """
    搜索文件
    """
    logger.info(f"Searching for {name}")
    return "not found"
