"""Extracts specific data from a web page."""

from google.adk.agents import Agent

from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mtlibs.adk_utils.callbacks import rate_limit_callback
from mtmai.tools.store_state import store_state_tool

from . import extract_page_data_agent_prompt

ExtractPageDataAgent = Agent(
    model=get_default_litellm_model(),
    name="extract_page_data_agent",
    description="Extract important data from the web page content",
    instruction=extract_page_data_agent_prompt.PROMPT,
    tools=[store_state_tool],
    before_model_callback=rate_limit_callback,
)
