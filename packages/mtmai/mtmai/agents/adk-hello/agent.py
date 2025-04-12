from google.adk.agents import Agent
from mtmai.model_client.utils import get_default_litellm_model

root_agent = Agent(
    name="weather_time_agent",
    model=get_default_litellm_model(),
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=("I can answer your questions about the time and weather in a city."),
    tools=[],
)
