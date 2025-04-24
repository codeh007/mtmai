from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mtlibs.id import generate_uuid
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


def before_agent_callback(callback_context: CallbackContext):
    current_state = callback_context.state.to_dict()
    callback_context.state["root_agent_init123444555"] = "root_agent_init456"
    instagram_username = current_state.get("inst:username")
    instagram_password = current_state.get("inst:password")

    if callback_context.user_content.parts[0].function_response:
        if callback_context.user_form.parts[0].function_call.name == "instagram_login":
            # logger.info(f"instagram_login: {callback_context.user_form.parts[0].function_call.args}")
            # 用户提交的登录凭据
            return types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="(后台运行) 正在登录 instagram 账号",
                    )
                ],
            )

    # 确保 instagram 登录凭据
    elif not instagram_username or not instagram_password:
        return types.Content(
            role="model",
            parts=[
                types.Part(
                    text="请登录",
                    function_call=types.FunctionCall(
                        id=generate_uuid(),
                        name="instagram_login",
                        args={
                            "username": instagram_username,
                            "password": instagram_password,
                        },
                    ),
                )
            ],
        )
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
        before_agent_callback=before_agent_callback,
    )
