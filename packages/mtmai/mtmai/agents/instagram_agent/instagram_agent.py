import json
from typing import Any, Optional, cast

import pyotp
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from loguru import logger
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtlibs.instagrapi import Client
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
    instagram_username = current_state.get("inst:username")
    instagram_password = current_state.get("inst:password")

    if callback_context.user_content.parts[0].function_response:
        function_response = cast(
            types.FunctionResponse,
            callback_context.user_content.parts[0].function_response,
        )
        if function_response.name == "instagram_login":
            ig_client = Client(
                # proxy=settings.default_proxy_url,
                proxy="socks5://US-Illinois-pbfBnijAfc-172.59.190.194:myb398a6ewyqcc5w@172.235.39.216:8000",
                request_timeout=3,
            )
            # 临时代码,用户注册
            signup_result = ig_client.signup(
                username=function_response.response.get("zhangxiaobin888"),
                password=function_response.response.get("ff12Abc4"),
                email=function_response.response.get("zhangxiaobin888@gmail.com"),
                phone_number=function_response.response.get("18810781012"),
                full_name="zhangxiaobin",
                year=1990,
                month=1,
                day=17,
            )
            logger.info(f"signup_result: {signup_result}")

            # 用户提交的登录凭据
            username = function_response.response.get("username")
            password = function_response.response.get("password")
            otp_key = function_response.response.get("otp_key")
            ig_client = Client(
                proxy=settings.default_proxy_url,
            )
            login_result = ig_client.login(
                username=username.strip(),
                password=password.strip(),
                verification_code=pyotp.TOTP(otp_key.strip().replace(" ", "")).now()
                if function_response.response.get("otp_key")
                else None,
                relogin=False,
            )

            if login_result:
                local_settings_file = f".vol/ig_settings_{username}.json"
                with open(local_settings_file, "w") as f:
                    f.write(json.dumps(login_result))
                login_data = ig_client.get_settings()
                callback_context.state.update({"ig_settings": login_data})
                ig_client.dump_settings(local_settings_file)
                return None

            return types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="instagram 登录失败",
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
