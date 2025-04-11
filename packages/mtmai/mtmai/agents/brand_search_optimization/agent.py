from google.adk.agents.llm_agent import Agent
from mtmai.agents.brand_search_optimization import prompt
from mtmai.agents.brand_search_optimization.shared_libraries import constants
from mtmai.agents.brand_search_optimization.sub_agents.comparison.agent import (
    comparison_root_agent,
)
from mtmai.agents.brand_search_optimization.sub_agents.keyword_finding.agent import (
    keyword_finding_agent,
)
from mtmai.agents.brand_search_optimization.sub_agents.search_results.agent import (
    search_results_agent,
)

root_agent = Agent(
    model=constants.MODEL,
    name=constants.AGENT_NAME,
    description=constants.DESCRIPTION,
    instruction=prompt.ROOT_PROMPT,
    sub_agents=[
        keyword_finding_agent,
        search_results_agent,
        comparison_root_agent,
    ],
)
