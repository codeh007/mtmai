import json
import os
from typing import Any, Optional, cast

import pyotp
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
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

    if not ig_settings:
        if os.path.exists(f".vol/ig_settings_{instagram_username}.json"):
            with open(f".vol/ig_settings_{instagram_username}.json", "r") as f:
                login_result = json.loads(f.read())
                state.update({"ig_settings": login_result})

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
                    # actions_with_update = EventActions(
                    #     state_delta={"ig_settings": login_result}
                    # )
                    # # 此事件可能代表内部系统操作，而不仅仅是智能体响应
                    # system_event = Event(
                    #     invocation_id="inv_login_update",
                    #     author="system",  # 或 'agent', 'tool' 等
                    #     actions=actions_with_update,
                    #     timestamp=time.time(),
                    #     # content 可能为 None 或表示所采取的操作
                    # )
                    # # --- 追加事件（这会更新状态） ---
                    # callback_context._invocation_context.session_service.append_event(
                    #     callback_context._invocation_context.session,
                    #     system_event,
                    # )
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
