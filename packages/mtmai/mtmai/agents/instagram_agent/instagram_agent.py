from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.instagram_tool import (
    instagram_account_info,
    instagram_follow_user,
    instagram_login,
    instagram_write_post,
)

from .instagram_prompts import get_instagram_instructions


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    if tool.name == "instagram_login":
        if tool_response["success"]:
            tool_context.state.update({"ig_settings": tool_response["result"]})

    if tool.name == "instagram_account_info":
        if tool_response["success"]:
            # tool_context.state["user_info"] = tool_response["result"]
            tool_context.state.update({"user_info": tool_response["result"]})
    return None


def new_instagram_agent():
    return LlmAgent(
        model=get_default_litellm_model(),
        name="instagram_agent",
        description="跟 instagram 社交媒体操作的专家",
        instruction=get_instagram_instructions(),
        tools=[
            instagram_login,
            instagram_write_post,
            instagram_account_info,
            instagram_follow_user,
        ],
        after_tool_callback=after_tool_callback,
    )
