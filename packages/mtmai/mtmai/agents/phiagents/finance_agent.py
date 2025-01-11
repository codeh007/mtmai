from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools

from mtmai.agents.phiagents.config import model
from mtmai.core.logging import get_logger

logger = get_logger()
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=model,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=["Always use tables to display data"],
    markdown=True,
    show_tool_calls=True,
)
