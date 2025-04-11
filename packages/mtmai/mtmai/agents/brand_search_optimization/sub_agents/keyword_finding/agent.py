"""Defines keyword finding agent."""

from google.adk.agents.llm_agent import Agent
from mtmai.agents.brand_search_optimization.shared_libraries import constants
from mtmai.agents.brand_search_optimization.sub_agents.keyword_finding import prompt

keyword_finding_agent = Agent(
    model=constants.MODEL,
    name="keyword_finding_agent",
    description="A helpful agent to find keywords",
    instruction=prompt.KEYWORD_FINDING_AGENT_PROMPT,
    tools=[
        # bq_connector.get_product_details_for_brand,
    ],
)
