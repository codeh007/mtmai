from typing import Any, Optional

from google.adk.agents import Agent
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.instagram_tool import instagram_login, instagram_write_post_tool
from mtmai.tools.store_state import store_state_tool

INSTAGRAM_AGENT_PROMPT = """你是 instagram 社交媒体操作的专家
背景:
    你拥有登录到 instagram 的账户基本信息,通过工具调用可以完成 instagram 的登录,以及登录后对账号的操作
    你是一个经验丰富的instagram 社交媒体操作专家, 你将使用 instagram 的 api 来操作 instagram 的账户
    根据用户的指令完成跟 instagram 相关的操作

## 工具调用
    - login_to_instagram: 登录到 instagram 的账户
    - post_to_instagram: 在 instagram 上发布帖子
    - follow_user: 关注其他用户
    - unfollow_user: 取消关注其他用户
    -

步骤建议:
    1: 登录到 instagram 的账户. 登录成功后, 保存登录信息到 state 中.
    2: 根据用户的指令完成跟 instagram 相关的操作.
    3: 当任务完成,或者出错无法继续时, 交接到 root_agent, 并且说明原因.
"""


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    if tool.name == "instagram_login":
        tool_context.state["ig_settings"] = tool_response

    return None


def new_instagram_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="instagram_agent",
        description="跟 instagram 社交媒体操作的专家",
        instruction=INSTAGRAM_AGENT_PROMPT,
        tools=[
            instagram_login,
            instagram_write_post_tool,
            store_state_tool,
        ],
        after_tool_callback=after_tool_callback,
    )


# def lowercase_value(value):
#     """Make dictionary lowercase"""
#     if isinstance(value, dict):
#         return (dict(k, lowercase_value(v)) for k, v in value.items())
#     elif isinstance(value, str):
#         return value.lower()
#     elif isinstance(value, (list, set, tuple)):
#         tp = type(value)
#         return tp(lowercase_value(i) for i in value)
#     else:
#         return value
