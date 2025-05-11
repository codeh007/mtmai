import json
import os
from typing import Any, Optional, cast

import pyotp
from fastapi.encoders import jsonable_encoder
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from mtmai.model_client import get_default_litellm_model
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtlibs.instagrapi import Client
from mtmai.tools.instagram_tool import (
    instagram_account_info,
    instagram_follow_user,
    instagram_login,
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
            tool_context.state["ig_settings"] = tool_response["result"]

    if tool.name == "instagram_account_info":
        if tool_response["success"]:
            # tool_context.state["user_info"] = tool_response["result"]
            tool_context.state["user_info"] = tool_response["result"]
    return None


def before_agent_callback(callback_context: CallbackContext):
    state = callback_context.state
    instagram_username = state.get("inst:username")
    instagram_password = state.get("inst:password")
    ig_settings = state.get("ig_settings")

    user_content = callback_context.user_content
    user_input_text = user_content.parts[0].text
    if user_input_text.startswith("/info"):
        proxy_url = callback_context.state.get("proxy_url")
        ig_client = Client()
        ig_settings = callback_context.state.get("ig_settings")
        if ig_settings:
            ig_client.set_settings(ig_settings)
        if proxy_url:
            ig_client.proxy = proxy_url
        account = ig_client.account_info()
        if account:
            callback_context.state["instagram_user_info"] = jsonable_encoder(
                account.model_dump()
            )
            return types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text=f"instagram 用户信息: {account.username}",
                    )
                ],
            )

    if user_input_text.startswith("/follow"):
        proxy_url = callback_context.state.get("proxy_url")
        ig_client = Client()
        ig_settings = callback_context.state.get("ig_settings")
        if ig_settings:
            ig_client.set_settings(ig_settings)
        if proxy_url:
            ig_client.proxy = proxy_url
        username = user_input_text.split(" ")[1]
        ig_client.dir()(username)
        return types.Content(
            role="assistant",
            parts=[types.Part(text=f"关注 {username} 成功")],
        )

    if callback_context.user_content.parts[0].function_response:
        function_response = cast(
            types.FunctionResponse,
            callback_context.user_content.parts[0].function_response,
        )
        if function_response.name == "instagram_login":
            # 临时代码,用户注册
            # signup_result = ig_client.signup(
            #     username=function_response.response.get("zhangxiaobin888"),
            #     password=function_response.response.get("ff12Abc4"),
            #     email=function_response.r esponse.get("zhangxiaobin888@gmail.com"),
            #     phone_number=function_response.response.get("18810781012"),
            #     full_name="zhangxiaobin",
            #     year=1990,
            #     month=1,
            #     day=17,
            # )
            # logger.info(f"signup_result: {signup_result}")

            # 如果本机已经存在 login settings

            # 用户提交的登录凭据
            username = function_response.response.get("username")
            state["username"] = username
            password = function_response.response.get("password")
            state["password"] = password
            otp_key = function_response.response.get("otp_key")
            state["otp_key"] = otp_key
            proxy_url = function_response.response.get("proxy_url")
            state["proxy_url"] = proxy_url
            if os.path.exists(f".vol/ig_settings_{username}.json"):
                with open(f".vol/ig_settings_{username}.json", "r") as f:
                    login_result = json.loads(f.read())
                    # （callback_context.state['key'] = value）会被跟踪并与回调后框架生成的事件相关联。
                    state["ig_settings"] = login_result
                    return types.Content(
                        role="assistant",
                        parts=[
                            types.Part(
                                text="instagram 登录成功",
                            )
                        ],
                    )
                    # return None
            ig_client = Client()
            if proxy_url:
                ig_client.proxy = proxy_url

            two_fa_code = None
            if otp_key:
                two_fa_code = pyotp.TOTP(otp_key.strip().replace(" ", "")).now()
            login_result = ig_client.login(
                username=username.strip(),
                password=password.strip(),
                verification_code=two_fa_code,
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

    # 要求登录
    elif not ig_settings:  # not instagram_username or not instagram_password:
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


def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    pass


def new_instagram_agent():
    return LlmAgent(
        model=get_default_litellm_model(),
        name="instagram_agent",
        description="跟 instagram 社交媒体操作的专家",
        instruction=get_instagram_instructions(),
        tools=[
            instagram_login,
            # instagram_write_post,
            instagram_account_info,
            instagram_follow_user,
        ],
        after_tool_callback=after_tool_callback,
        before_agent_callback=before_agent_callback,
        before_model_callback=before_model_callback,
        output_key="last_instagram_agent_output",
    )
