import uuid

import structlog
from agents.nodes import pop_dialog_state
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from mtmai.agents.graphutils import (
    create_tool_node_with_fallback,  # is_internal_node,; is_skip_kind,
)
from mtmai.agents.nodes.assisant_node import (
    AssistantNode,
    primary_assistant_tools,
    route_assistant,
)

from ..states import MtmState

LOG = structlog.get_logger()

# 参考：
# https://github.com/gitroomhq/postiz-app/blob/main/libraries/nestjs-libraries/src/agent/agent.graph.service.ts


class AssistantGraph:
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

    @staticmethod
    async def run(input: MtmState, thread_id: str | None = None):
        builded_graph = await AssistantGraph().build_graph()

        if not thread_id:
            thread_id = str(uuid.uuid4())
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.store.memory import InMemoryStore

        mem_checkpointer = MemorySaver()
        mem_store = InMemoryStore()
        graph = builded_graph.compile(
            checkpointer=mem_checkpointer,
            store=mem_store,
            # interrupt_after=["human"],
            interrupt_before=[
                # HUMEN_INPUT_NODE,
            ],
            debug=True,
        )

        image_data = graph.get_graph(xray=1).draw_mermaid_png()
        save_to = "./.vol/postiz-graph.png"
        with open(save_to, "wb") as f:
            f.write(image_data)

        inputs = {
            # "messages": messages,
            # "userId": user_id,
            # "params": params,
            "topic": "seo",
        }
        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            # yield aisdk.data(event)
            # if not is_internal_node(node_name):
            #     if not is_skip_kind(kind):
            #         logger.info("[event] %s@%s", kind, node_name)

            # if kind == "on_chat_model_stream":
            #     content = event["data"]["chunk"].content
            #     if content:
            #         yield aisdk.text(content)

        return {"fresearch": "xxxxxxxxxxfresearchxxxxxxxxxxxx"}
