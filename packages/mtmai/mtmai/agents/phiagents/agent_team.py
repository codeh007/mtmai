from phi.agent import Agent

from mtmai.agents.phiagents.config import model
from mtmai.agents.phiagents.finance_agent import finance_agent
from mtmai.agents.phiagents.web_agent import web_agent
from mtmai.core.logging import get_logger

logger = get_logger()
agent_team = Agent(
    team=[web_agent, finance_agent],
    show_tool_calls=True,
    markdown=True,
    model=model,
    monitoring=True,
    add_history_to_messages=True,
    read_chat_history=True,
    # debug_mode=True,
)
