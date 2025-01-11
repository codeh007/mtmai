from typing import Annotated, Literal

import structlog
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel

from mtmai.agents.graphutils import (  # is_internal_node,; is_skip_kind,
    create_tool_node_with_fallback,
    pop_dialog_state,
)
from mtmai.agents.nodes.assisant_node import (
    AssistantNode,
    primary_assistant_tools,
    route_assistant,
)
from mtmai.models.task import MtTask


class UiState(BaseModel):
    showWorkbench: bool | None = None
    currentWorkbenchView: str | None = None


class ArticleArtifact(BaseModel):
    id: str
    content: str
    title: str
    type: Literal["code", "text"]
    language: str


class MtmState(BaseModel):
    messages: Annotated[list, add_messages] = []
    uiState: UiState = UiState()
    scheduleId: str | None = None
    taskId: str | None = None
    next: str | None = None
    userId: str | None = None
    artifacts: list[ArticleArtifact] = []
    task_data: MtTask | None = None
    user_input: str | None = None

    # human 节点直接输出给前端用户的消息
    human_ouput_message: str | None = None
    is_debug: bool | None = False
    task_config: dict | None = None


LOG = structlog.get_logger()


class MtmAssistantGraph:
    def __init__(self):
        pass

    @property
    def name(self):
        return "assistant"

    @property
    def description(self):
        return "直接面向用户的聊天机器人助手"

    async def build_graph(self):
        wf = StateGraph(MtmState)

        wf.add_node("entry", AssistantNode())
        wf.set_entry_point("entry")
        wf.add_conditional_edges(
            "entry",
            route_assistant,
            [
                "articleGen",
                # HUMEN_INPUT_NODE,
                "assistant",
                # "site",
                "create_task",
            ],
        )

        wf.add_node("assistant", AssistantNode())

        wf.add_conditional_edges(
            "assistant",
            tools_condition,
        )

        wf.add_node(
            "tools",
            create_tool_node_with_fallback(primary_assistant_tools),
        )
        wf.add_conditional_edges(
            "tools",
            route_assistant,
            {
                "assistant": "assistant",
                # "error": END,
            },
        )
        # wf.add_node(HUMEN_INPUT_NODE, HumanInputNode())
        # wf.add_edge(HUMEN_INPUT_NODE, "assistant")

        # wf.add_node("articleGen", ArticleGenNode())
        # wf.add_edge("articleGen", HUMEN_INPUT_NODE)

        wf.add_node("leave_skill", pop_dialog_state)
        wf.add_edge("leave_skill", "assistant")

        # wf.add_node("site", SiteNode())
        # wf.add_edge("site", "assistant")

        # wf.add_node("create_task", CreateTaskNode())
        # wf.add_edge("create_task", "assistant")

        return wf
