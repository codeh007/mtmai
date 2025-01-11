from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import tools_condition

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.graphutils import (
    CompleteOrEscalate,
    create_entry_node,
    create_tool_node_with_fallback,
)
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()

develop_safe_tools = []
develop_sensitive_tools = []
develop_tools = develop_safe_tools + develop_sensitive_tools


def route_develop_mode(
    state: HomeChatState,
):
    route = tools_condition(state.messages)
    if route == END:
        return END
    tool_calls = state.messages[-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    safe_toolnames = [t.name for t in develop_safe_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "develop_safe_tools"
    return "develop_sensitive_tools"


class DevelopNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "develop_node"

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        develop_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a specialized assistant for handling development tasks. "
                    "The primary assistant delegates work to you whenever the user needs help with development-related queries or tasks. "
                    "You can use various tools to assist developers, such as reading logs, retrieving system status information, and performing other development-related actions. "
                    "Be thorough and precise in your responses, providing detailed information when necessary. "
                    "If a task requires multiple steps, guide the user through each step clearly. "
                    "If you need more information or if the task is beyond your capabilities, escalate the task back to the main assistant. "
                    "Remember to use the appropriate tools for each task and provide clear explanations of your actions. "
                    "Always prioritize security and best practices in your recommendations."
                    "\nCurrent time: {time}."
                    "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
                    ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.'
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())

        # develop_runnable = develop_prompt | self.runnable.bind_tools(
        #     develop_tools + [CompleteOrEscalate]
        # )
        return {
            "messages": await mtmai_context.ainvoke_model(
                develop_prompt, state, tools=develop_tools + [CompleteOrEscalate]
            )
        }

    @classmethod
    async def addto_primary_assistant(self, wf: StateGraph):
        llm_runnable = await mtmai_context.get_llm_openai("chat")

        wf.add_node(
            "enter_develop_mode",
            create_entry_node("Developer Mode & Development Assistant", "develop_mode"),
        )
        wf.add_node("develop_mode", DevelopNode(llm_runnable))
        wf.add_edge("enter_develop_mode", "develop_mode")
        wf.add_node(
            "develop_sensitive_tools",
            create_tool_node_with_fallback(develop_sensitive_tools),
        )
        wf.add_node(
            "develop_safe_tools",
            create_tool_node_with_fallback(develop_safe_tools),
        )

        wf.add_edge("develop_sensitive_tools", "develop_mode")
        wf.add_edge("develop_safe_tools", "develop_mode")
        wf.add_conditional_edges(
            "develop_mode",
            route_develop_mode,
            [
                "develop_sensitive_tools",
                "develop_safe_tools",
                "leave_skill",
                # END,
            ],
        )
