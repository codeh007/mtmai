from typing import Any, Optional

from google.adk.agents import Agent
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

            # --- Define State Changes ---
            # current_time = time.time()
            # state_changes = {
            #     "task_status": "active",  # Update session state
            #     "user:login_count": tool_context.state.get("user:login_count", 0)
            #     + 1,  # Update user state
            #     "user:last_login_ts": current_time,  # Add user state
            #     "temp:validation_needed": True,  # Add temporary state (will be discarded)
            # }

            # # --- Create Event with Actions ---
            # actions_with_update = EventActions(state_delta=state_changes)
            # # This event might represent an internal system action, not just an agent response
            # system_event = Event(
            #     invocation_id="inv_login_update",
            #     author="system",  # Or 'agent', 'tool' etc.
            #     actions=actions_with_update,
            #     timestamp=current_time,
            #     # content might be None or represent the action taken
            # )
            # return system_event

            # --- Append the Event (This updates the state) ---
            # session_service.append_event(session, system_event)
    if tool.name == "instagram_account_info":
        if tool_response["success"]:
            # tool_context.state["user_info"] = tool_response["result"]
            tool_context.state.update({"user_info": tool_response["result"]})
    return None


def new_instagram_agent():
    return Agent(
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
