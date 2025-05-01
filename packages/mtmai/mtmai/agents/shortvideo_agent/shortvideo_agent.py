from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from loguru import logger
from mtmai.agents.shortvideo_agent.shortvideo_prompts import get_shortvideo_instructions
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mpt.models.schema import VideoAspect, VideoParams
from mtmai.mpt.services.task import start_gen_video


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    return None


def before_agent_callback(callback_context: CallbackContext):
    user_content = callback_context.user_content
    user_input_text = user_content.parts[0].text
    if user_input_text.startswith("/test1"):
        try:
            result = start_gen_video(
                "01",
                VideoParams(
                    video_subject="video_subject123",
                    video_script="my 123",
                    video_terms="video_terms123",
                    video_aspect=VideoAspect.landscape,
                    voice_name="女生-晓晓",
                    bgm_name="random",
                    # font_name="STHeitiMedium 黑体-中",
                    text_color="#FFFFFF",
                    font_size=60,
                    stroke_color="#000000",
                ),
            )
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
