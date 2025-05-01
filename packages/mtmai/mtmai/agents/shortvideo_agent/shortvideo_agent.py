import asyncio
from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from loguru import logger
from mtmai.agents.shortvideo_agent.shortvideo_prompts import get_shortvideo_instructions
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mpt.services.task import hello123333


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    return None


agent_event_loop = asyncio.get_event_loop()


def before_agent_callback(callback_context: CallbackContext):
    user_content = callback_context.user_content
    user_input_text = user_content.parts[0].text
    if user_input_text.startswith("/test1"):
        try:
            # 获取当前事件循环
            # loop = asyncio.get_event_loop()
            # if loop.is_running():
            #     # 如果事件循环正在运行，创建一个新的事件循环
            #     loop = asyncio.new_event_loop()
            #     # asyncio.set_event_loop(loop)
            # loop = asyncio.get_event_loop()

            # 使用 run_coroutine_threadsafe 来运行异步代码
            # future = asyncio.run_coroutine_threadsafe(
            #     start_gen_video(
            #         "01",
            #         VideoParams(
            #             video_subject="video_subject123",
            #             video_script="my 123",
            #             video_terms="video_terms123",
            #             video_aspect=VideoAspect.landscape,
            #             bgm_name="random",
            #             text_color="#FFFFFF",
            #             font_size=60,
            #             stroke_color="#000000",
            #         ),
            #     ),
            #     loop,
            # )
            # 等待结果
            # result = future.result()
            # result = asyncio.run(
            #     # start_gen_video(
            #     #     "01",
            #     #     VideoParams(
            #     #         video_subject="video_subject123",
            #     #         video_script="my 123",
            #         video_terms="video_terms123",
            #         video_aspect=VideoAspect.landscape,
            #         bgm_name="random",
            #         text_color="#FFFFFF",
            #         font_size=60,
            #         stroke_color="#000000",
            #     ),
            # )
            #     hello123333()
            # )
            result = agent_event_loop.run_until_complete(hello123333())
            logger.info(f"result: {result}")
        except Exception as e:
            logger.error(f"error: {e}")

    return None


def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    pass


def new_shortvideo_agent():
    return LlmAgent(
        model=get_default_litellm_model(),
        name="shortvideo_agent",
        description="短视频生成专家",
        instruction=get_shortvideo_instructions(),
        tools=[
            # instagram_login,
            # instagram_write_post,
            # instagram_account_info,
            # instagram_follow_user,
        ],
        after_tool_callback=after_tool_callback,
        before_agent_callback=before_agent_callback,
        before_model_callback=before_model_callback,
        output_key="last_shortvideo_agent_output",
    )
