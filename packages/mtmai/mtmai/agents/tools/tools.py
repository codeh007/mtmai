import structlog
from crewai.tools.base_tool import Tool
from mtmai.agents.tools.web_search import search_engine
from pydantic import BaseModel, Field

LOG = structlog.get_logger()


class ToFlightBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle flight updates and cancellations."""

    request: str = Field(
        description="Any necessary followup questions the update flight assistant should clarify before proceeding."
    )


class ToBookCarRental(BaseModel):
    """Transfers work to a specialized assistant to handle car rental bookings."""

    location: str = Field(
        description="The location where the user wants to rent a car."
    )
    start_date: str = Field(description="The start date of the car rental.")
    end_date: str = Field(description="The end date of the car rental.")
    request: str = Field(
        description="Any additional information or requests from the user regarding the car rental."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Basel",
                "start_date": "2023-07-01",
                "end_date": "2023-07-05",
                "request": "I need a compact car with automatic transmission.",
            }
        }


def get_tools(tools_name: str | list[str]):
    """
    根据工具名称获取工具函数
    """
    tools = []
    if isinstance(tools_name, str):
        tools_name = [tools_name]

    for tool_name in tools_name:
        if tool_name == "search_engine":
            # tools.append(Tool.from_langchain(search_engine_tool))
            tools.append(Tool.from_langchain(search_engine))
    return tools
