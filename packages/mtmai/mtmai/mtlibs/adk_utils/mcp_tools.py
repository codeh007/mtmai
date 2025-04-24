from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from loguru import logger


async def get_mcp_tools_async():
    """从MCP服务器获取工具"""
    logger.info("尝试连接到MCP服务器...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="python3",
            args=["-m", "mcp_server_fetch"],
        )
    )
    logger.info("MCP Toolset 创建成功.")
    # MCP 需要维持与本地MCP服务器的连接
    # exit_stack 管理这个连接的清理
    return tools, exit_stack
