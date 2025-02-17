import random

from autogen_core.tools import FunctionTool
from loguru import logger
from typing_extensions import Annotated


async def get_stock_price(
    ticker: str, date: Annotated[str, "Date in YYYY/MM/DD"]
) -> float:
    # Returns a random stock price for demonstration purposes.
    return random.uniform(10, 200)


# example
stock_price_tool = FunctionTool(get_stock_price, description="Get the stock price.")

# Run the tool.
# cancellation_token = CancellationToken()
# result = await stock_price_tool.run_json({"ticker": "AAPL", "date": "2021/01/01"}, cancellation_token)

# Print the result.
# print(stock_price_tool.return_value_as_string(result))


async def hf_space_reset():
    logger.info("Resetting HF Space=====================================")


hf_space_reset_tool = FunctionTool(hf_space_reset, description="Reset HF Space")
