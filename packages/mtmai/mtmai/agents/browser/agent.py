import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Dict

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import Event, EventActions
from google.adk.tools import BaseTool, ToolContext
from google.genai import types
from loguru import logger
from mtmai.model_client.utils import get_default_litellm_model
from pydantic import BaseModel


# ============ Configuration Section ============
@dataclass
class TwitterConfig:
    """Configuration for Twitter posting"""

    openai_api_key: str
    chrome_path: str
    target_user: str  # Twitter handle without @
    message: str
    reply_url: str
    headless: bool = False
    model: str = "gpt-4o-mini"
    base_url: str = "https://x.com/home"


# Customize these settings
config = TwitterConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # This is for MacOS (Chrome)
    target_user="XXXXX",
    message="XXXXX",
    reply_url="XXXXX",
    headless=False,
)


class HelloModel1(BaseModel):
    name: str
    age: int


def before_agent_callback(callback_context: CallbackContext):
    """
    在 agent 执行前, 设置获取或者初始化浏览器配置
    """
    # callback_context.state.update(
    #     {
    #         "browser_config": {
    #             "browser_type": "chrome",
    #             "browser_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    #         }
    #     }
    # )
    # return None
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    print(f"[Callback] Entering agent: {agent_name} (Invocation: {invocation_id})")

    # Example: Check a condition in state
    if callback_context.state.get("skip_agent", False):
        print(f"[Callback] Condition met: Skipping agent {agent_name}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} was skipped by callback.")]
        )
    else:
        print(f"[Callback] Condition not met: Proceeding with agent {agent_name}.")
        # Return None to allow the agent's run to execute

        # callback_context.state.update(
        #     {
        #         "browser_config": {
        #             "browser_type": "chrome",
        #             "browser_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        #         }
        #     }
        # )
        state_changes = {
            "task_status": "active",  # Update session state
            # "user:login_count": session.state.get("user:login_count", 0) + 1, # Update user state
            # "user:last_login_ts": current_time,   # Add user state
            # "temp:validation_needed": True        # Add temporary state (will be discarded)
        }

        # --- Create Event with Actions ---
        actions_with_update = EventActions(state_delta=state_changes)
        # This event might represent an internal system action, not just an agent response
        system_event = Event(
            invocation_id="inv_login_update",
            author="system",  # Or 'agent', 'tool' etc.
            actions=actions_with_update,
            # timestamp=current_time
            # content might be None or represent the action taken
        )

        # --- Append the Event (This updates the state) ---
        # callback_context.session_service.append_event(session, system_event)
        # callback_context.state.update(
        #     {
        #         "browser_config444agent_init": {
        #             "browser_type": "chrome",
        #             "browser_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        #         }
        #     }
        # )
        return None


def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
):
    """
    在 tool 执行前, 设置获取或者初始化浏览器配置
    """
    agent_name = tool_context.agent_name
    tool_name = tool.name
    # print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    # print(f"[Callback] Original args: {args}")

    if tool_name == "browser_use_tool" or tool_name == "browser_use_steal_tool":
        # 调用浏览器工具前, 先初始化 浏览器配置, 包括 浏览器指纹, 网络代理, 浏览器配置
        logger.warning(
            "TODO: 调用浏览器工具前, 先初始化 浏览器配置, 包括 浏览器指纹, 网络代理, 浏览器配置"
        )
        # 可以这样设置 state
        # tool_context.state.update({"browser_config222": {"browser_type": "chrome"}})
    return None


def after_tool_callback(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
):
    """
    在 tool 执行后, 设置获取或者初始化浏览器配置
    """
    logger.warning(f"tool_response: {tool_response}")


def create_browser_agent():
    from mtmai.tools.browser_tool import browser_use_steal_tool, browser_use_tool

    return Agent(
        model=get_default_litellm_model(),
        name="web_browser_agent",
        description="网页浏览器操作助理,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务",
        instruction=dedent(
            """你是专业操作浏览器的助手,擅长根据用户的对话上下文调用工具完成用户的指定任务.
**重要**:
    - 工具是开源 browser use, 版本号是 v0.1.40, 你必须一次性通过自然语音的描述将完整的任务交代清楚,
    - browser use 本身是 ai agent 可以理解你的任务并且内部能智能规划通过多个步骤操作浏览器来完成你给出的任务.
    - browser use 在任务结束后给你返回任务的最终结果描述, 并且会将任务的相关状态保存. 你可以在下一轮对话中获取到任务的结果的详细描述以及关键状态数据
    - 如果任务需要一些基本的资料, 应该在任务描述中附带. 特别是 账号, 网址, 等等.
    - 你需要完全明白浏览器所需的任务规划, 给出经过优化的步骤规划指引 browser use 操作
    - 你需要完全了解用户的意图以及任务涉及网站的相关特性

工具指引:
    browser_use_tool: 用于完成通用浏览器操作任务
    browser_use_steal_tool: 创建独立浏览器配置文件, 使用特定的 网络代理 和 浏览器指纹配置,防止账号间关联
"""
        ),
        tools=[browser_use_tool, browser_use_steal_tool],
        before_agent_callback=before_agent_callback,
        before_tool_callback=before_tool_callback,
    )
