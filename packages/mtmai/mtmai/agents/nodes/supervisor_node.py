from enum import member
from textwrap import dedent
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel

from mtmai.models.graph_config import HomeChatState, MainState



def edge_supervisor(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    next_to = state.get("next")
    if next_to:
        return next_to
    return "__end__"


members = ["human_chat", "JokeWriter"]

class RouteResponse(BaseModel):
    next: Literal["human_chat", "JokeWriter"]

# supervisor_prompt = dedent("""
# Given the conversation above, who should act next?
# Or should we FINISH? Select one of: {options}
# """)


class SupervisorNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def agent_name(self):
        return "Supervisor"

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        options = member
        supervisor_system_prompt = (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers:  {members}. \n"
            "Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
        )

        options = [*members]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", supervisor_system_prompt),
                MessagesPlaceholder(variable_name="messages", optional=True),
                (
                    "system",
                    "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))

        supervisor_chain = prompt | self.runnable.with_structured_output(RouteResponse)
        result = await supervisor_chain.ainvoke(state.model_dump())
        return {
            "next": result.next
        }
