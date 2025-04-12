import asyncio

from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types
from loguru import logger


async def get_tools_async():
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


async def get_agent_async():
    """创建一个配备了MCP服务器工具的ADK代理"""
    tools, exit_stack = await get_tools_async()
    logger.info(f"从MCP服务器获取了 {len(tools)} 个工具.")

    root_agent = LlmAgent(
        model="gemini-2.0-flash",  # 根据可用性调整模型名称
        name="fetch_assistant",
        instruction="使用可用工具帮助用户从网页中提取内容.",
        tools=tools,  # 将MCP工具提供给ADK代理
    )
    return root_agent, exit_stack


async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name="mcp_fetch_app", user_id="user_fetch"
    )

    # 设置查询
    query = "从 https://example.com 提取内容"
    logger.info(f"用户查询: '{query}'")
    content = types.Content(role="user", parts=[types.Part(text=query)])

    root_agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name="mcp_fetch_app",
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    logger.info("运行代理中...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        logger.info(f"收到事件: {event}")

    # 关键清理步骤: 确保MCP服务器进程连接已关闭
    logger.info("关闭MCP服务器连接...")
    await exit_stack.aclose()
    logger.info("清理完成.")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        logger.error(f"发生错误: {e}")
