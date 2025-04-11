import datetime

from google.adk.agents import Agent
from loguru import logger
from mtmai.model_client.utils import get_default_litellm_model
from zoneinfo import ZoneInfo


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    logger.error(f"Getting weather for {city}")
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
        # 明确的工具调用错误
        # return {
        #     "status": "error",
        #     "error_message": f"Weather information for '{city}' is not available.",
        # }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    logger.error(f"Getting current time for {city}")

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        tz_identifier = "America/New_York"
        # 明确的工具调用错误
        # return {
        #     "status": "error",
        #     "error_message": (f"Sorry, I don't have timezone information for {city}."),
        # }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model=get_default_litellm_model(),
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=("I can answer your questions about the time and weather in a city."),
    tools=[get_weather, get_current_time],
)
