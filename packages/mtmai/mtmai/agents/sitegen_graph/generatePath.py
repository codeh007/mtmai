from datetime import datetime

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.opencanvas.opencanvas_state import OpenCanvasState
from mtmai.agents.sitegen_graph.sitegen_state import AssistantState
from mtmai.core.logging import get_logger

logger = get_logger()


class RouteQueryResult(BaseModel):
    route: str
    artifactId: str | None = None


def routeGeneratePath(state: OpenCanvasState):
    # is_tools = tools_condition(state)
    # if is_tools == "tools":
    #     return "chat_tools_node"
    if not state.next:
        raise ValueError("state.next not set")
    # next_to = state.get("next")
    # if next_to:
    #     return next_to
    return state.next


class GeneratePath:
    """
    根据状态选择下一节点
    """

    def __init__(self):
        pass

    async def get_prompt(self, state: AssistantState):
        primary_assistant_prompt = ChatPromptTemplate.from_messages(
            [
                # (
                #     "system",
                #     "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                #     "Your primary role is to search for flight information and company policies to answer customer queries. "
                #     "If a customer requests to update or cancel a flight, book a car rental, book a hotel, or get trip recommendations, "
                #     "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                #     " Only the specialized assistants are given permission to do this for the user."
                #     "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                #     "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                #     " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                #     " If a search comes up empty, expand your search before giving up."
                #     "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                #     "\n 必须使用中文回复用户"
                #     "\nCurrent time: {time}."
                #     "{additional_instructions}",
                # ),
                (
                    "system",
                    "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                    "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                    " Only the specialized assistants are given permission to do this for the user."
                    "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                    "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    " If a search comes up empty, expand your search before giving up."
                    "\n 必须使用中文回复用户"
                    "\nCurrent time: {time}."
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())
        return primary_assistant_prompt

    async def __call__(self, state: OpenCanvasState, config: RunnableConfig):
        # 临时代码
        # 展示一直置项 SiteNode
        # return {
        #     "next": "SiteNode",
        # }
        messages = state.messages

        # 如果有明确的状态，例如用户选定了一些文字，选定了一些组件。
        if state.highlighted:
            return {
                "next": "updateArtifact",
                "selectedArtifactId": state.highlighted.id,
            }

        # 如果没有明确状态，就调用 llm 决定下一个节点
        parser = PydanticOutputParser(pydantic_object=RouteQueryResult)

        route_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                    "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                    " Only the specialized assistants are given permission to do this for the user."
                    "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                    "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    " If a search comes up empty, expand your search before giving up."
                    "\n 必须使用中文回复用户"
                    "\nCurrent time: {time}."
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(
            time=datetime.now(),
            additional_instructions="",
            # recentMessages=messages,
            # artifacts="",
            # selectedArtifact="",
        )

        result = await mtmai_context.ainvoke_model_with_structured_output(
            route_prompt,
            state,
            structured_output=RouteQueryResult,
        )
        if result is None:
            return {
                "next": "respondToQuery",
            }

        if result.get("parsing_error"):
            logger.error(f"parsing_error: {result.parsing_error}")
        next = result["parsed"].route
        if next == "updateArtifact":
            selectedArtifactId = result.artifactId
        return {
            "next": next,
        }
