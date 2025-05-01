from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from mtmai.agents.shortvideo_agent.shortvideo_prompts import get_shortvideo_instructions
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.instagram_tool import instagram_login


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    return None


def before_agent_callback(callback_context: CallbackContext):
    return None


def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    pass


def new_shortvideo_agent():
    return LlmAgent(
        model=get_default_litellm_model(),
        name="shortvideo_agent",
        description="跟 shortvideo 社交媒体操作的专家",
        instruction=get_shortvideo_instructions(),
        tools=[
            instagram_login,
            # instagram_write_post,
            # instagram_account_info,
            # instagram_follow_user,
        ],
        after_tool_callback=after_tool_callback,
        before_agent_callback=before_agent_callback,
        before_model_callback=before_model_callback,
        output_key="last_shortvideo_agent_output",
    )
