from google.adk.agents import Agent

from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.weatherapi import get_current_time, get_weather

root_agent = Agent(
    name="weather_time_agent",
    model=get_default_litellm_model(),
    description=("智能助手，可以回答关于各个城市的天气和时间问题。"),
    instruction=(
        "我是一个能够提供城市天气和时间信息的智能助手。"
        "当用户询问某个城市的天气情况时，使用get_weather工具获取最新天气数据。"
        "当用户询问某个城市的当前时间时，使用get_current_time工具获取准确时间。"
        "请以友好的方式回应用户的询问，并提供完整的天气或时间信息。"
        "我能够理解中文城市名称，并自动转换为对应的英文名。"
    ),
    tools=[get_weather, get_current_time],
)
