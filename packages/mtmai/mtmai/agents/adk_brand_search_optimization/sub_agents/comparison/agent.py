from google.adk.agents.llm_agent import Agent
from mtmai.agents.adk_brand_search_optimization.shared_libraries import constants
from mtmai.agents.adk_brand_search_optimization.sub_agents.comparison import prompt


def new_comparison_root_agent():
    comparison_generator_agent = Agent(
        model=constants.MODEL,
        name="comparison_generator_agent",
        description="A helpful agent to generate comparison.",
        instruction=prompt.COMPARISON_AGENT_PROMPT,
    )

    comparsion_critic_agent = Agent(
        model=constants.MODEL,
        name="comparison_critic_agent",
        description="A helpful agent to critique comparison.",
        instruction=prompt.COMPARISON_CRITIC_AGENT_PROMPT,
    )

    comparison_root_agent = Agent(
        model=constants.MODEL,
        name="comparison_root_agent",
        description="A helpful agent to compare titles",
        instruction=prompt.COMPARISON_ROOT_AGENT_PROMPT,
        sub_agents=[comparison_generator_agent, comparsion_critic_agent],
    )
    return comparison_root_agent
