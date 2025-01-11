import uuid

import structlog
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import tools_condition

from mtmai.agents.ctx import init_mtmai_http_context, mtmai_context
from mtmai.agents.graphutils import (
    create_tool_node_with_fallback,
    is_internal_node,
    is_skip_kind,
    pop_dialog_state,
)
from mtmai.agents.task_graph.nodes.article_gen_node import ArticleGenNode
from mtmai.agents.task_graph.nodes.assisant_node import (
    PrimaryAssistantNode,
    primary_assistant_tools,
    route_assistant,
)
from mtmai.agents.task_graph.nodes.create_task_node import CreateTaskNode
from mtmai.agents.task_graph.nodes.human_input_node import HumanInputNode
from mtmai.agents.task_graph.nodes.site_node import SiteNode
from mtmai.agents.task_graph.nodes.task_entry_node import TaskEntryNode, routeEntryPath
from mtmai.agents.task_graph.task_state import TaskState

LOG = structlog.get_logger()

HUMEN_INPUT_NODE = "human_input"


class TaskGraph:
    def __init__(self):
        pass

    @classmethod
    def name(cls):
        return "blog_graph"

    async def build_graph(self):
        wf = StateGraph(TaskState)

        wf.add_node("entry", TaskEntryNode())
        wf.set_entry_point("entry")
        wf.add_conditional_edges(
            "entry",
            routeEntryPath,
            [
                "articleGen",
                HUMEN_INPUT_NODE,
                "assistant",
                "site",
                "create_task",
            ],
        )

        wf.add_node("assistant", PrimaryAssistantNode())

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
        wf.add_node(HUMEN_INPUT_NODE, HumanInputNode())
        wf.add_edge(HUMEN_INPUT_NODE, "assistant")

        wf.add_node("articleGen", ArticleGenNode())
        wf.add_edge("articleGen", HUMEN_INPUT_NODE)

        wf.add_node("leave_skill", pop_dialog_state)
        wf.add_edge("leave_skill", "assistant")

        wf.add_node("site", SiteNode())
        wf.add_edge("site", "assistant")

        wf.add_node("create_task", CreateTaskNode())
        # wf.add_edge("create_task", "assistant")

        return wf

    # async def compile_graph(self) -> CompiledGraph:
    #     graph = (await self.build_graph()).compile(
    #         checkpointer=await mtmai_context.get_graph_checkpointer(),
    #         # interrupt_after=["human"],
    #         interrupt_before=[
    #             HUMEN_INPUT_NODE,
    #         ],
    #         debug=True,
    #     )

    #     if is_in_dev():
    #         image_data = graph.get_graph(xray=1).draw_mermaid_png()
    #         save_to = "./.vol/taskrunner_graph.png"
    #         with open(save_to, "wb") as f:
    #             f.write(image_data)
    #     return graph

    # async def getExampleState(self):
    #     state = {
    #         "messages": [],
    #         "task_config": {
    #             "siteUrl": "https://www.baidu.com",
    #         },
    #     }
    #     return state

    async def on_chat_resume(self):
        init_mtmai_http_context()
        # thread_id = context.session.thread_id
        # user_session = cl.user_session
        # thread_id = context.session.thread_id
        # await cl.Message(content="正在恢复对话").send()
        graph = await TaskGraph().compile_graph()
        # user_session.set("graph", graph)

        # context.session.has_first_interaction = True
        # if not graph:
        #     cl.Message(content="工作流初始化失败").send()
        #     raise ValueError("graph 未初始化")

        thread: RunnableConfig = {
            "configurable": {
                # "thread_id": thread_id,
            }
        }
        pre_state = await graph.aget_state(thread, subgraphs=True)
        # LOG.info("()on_chat_resume %s", thread_id)

        # all_steps = await curd_chat.get_steps_by_thread(thread_id)
        # LOG.info("all_steps %s", all_steps)

    async def onRequest(self, inputs=None, messages=None, thread_id=None):
        graph = await TaskGraph().compile_graph()
        if not graph:
            raise ValueError("graph 未初始化")

        if not thread_id:
            thread_id = str(uuid.uuid4())

        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
                # 可以从指定检测点运行，以及分支
                # "checkpoint_id": "xxxxx"
            }
        }
        await self.run_graph(thread, graph, inputs, messages)

    async def run_graph(
        self, thread: RunnableConfig, graph: CompiledGraph, inputs=None, messages=None
    ):
        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            if not is_internal_node(node_name):
                if not is_skip_kind(kind):
                    LOG.info("[event] %s@%s", kind, node_name)
                    mtmai_context.emit("logs", {"on": kind, "node_name": node_name})

            if kind == "on_chat_model_stream":
                yield data

            if kind == "on_chain_start":
                LOG.info("on_chain_start %s:", node_name)
                output = data.get("output")
                if node_name == "__start__":
                    pass

            if kind == "on_chain_end":
                LOG.info("on_chain_end %s:", node_name)
                output = data.get("output")
                if node_name == "__start__":
                    pass
                if node_name in [HUMEN_INPUT_NODE, "articleGen", "entry"]:
                    human_ouput_message = output.get("human_ouput_message")
                    LOG.info("human_ouput_message %s", human_ouput_message)
            if node_name == "on_chat_start_node":
                thread_ui_state = output.get("thread_ui_state")

            if kind == "on_tool_start":
                pass

            if kind == "on_tool_end":
                output = data.get("output")
                pass
