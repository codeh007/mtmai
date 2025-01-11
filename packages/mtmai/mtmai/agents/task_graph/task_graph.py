import traceback
import uuid

import structlog
from fastapi.encoders import jsonable_encoder
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import tools_condition
from langgraph.types import StateSnapshot

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
from mtmai.core.coreutils import is_in_dev
from mtmai.crud import curd_chat

LOG = structlog.get_logger()

HUMEN_INPUT_NODE = "human_input"


class TaskGraph:
    def __init__(self):
        pass

    @classmethod
    def name(cls):
        return "taskrunner"

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

    async def compile_graph(self) -> CompiledGraph:
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human"],
            interrupt_before=[
                HUMEN_INPUT_NODE,
                # "update_flight_sensitive_tools",
                # "develop_sensitive_tools",
                # "book_car_rental_sensitive_tools",
                # "book_hotel_sensitive_tools",
                # "book_excursion_sensitive_tools",
            ],
            debug=True,
        )

        if is_in_dev():
            image_data = graph.get_graph(xray=1).draw_mermaid_png()
            save_to = "./.vol/taskrunner_graph.png"
            with open(save_to, "wb") as f:
                f.write(image_data)
        return graph

    async def getExampleState(self):
        state = {
            "messages": [],
            "task_config": {
                "siteUrl": "https://www.baidu.com",
            },
        }
        return state

    async def chat_start(self):
        init_mtmai_http_context()
        user_session = cl.user_session
        user = user_session.get("user")
        thread_id = context.session.thread_id
        # await cl.Message(content="欢迎使用博客文章生成器").send()
        graph = await TaskGraph().compile_graph()
        user_session.set("graph", graph)

        context.session.has_first_interaction = True
        await context.emitter.emit(
            "first_interaction",
            {
                "interaction": "graph_start",
                "thread_id": context.session.thread_id,
            },
        )
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        # await self.run_graph(thread, {"messages": []})
        await self.run_graph(thread, await self.getExampleState())

    async def on_chat_resume(self):
        init_mtmai_http_context()
        thread_id = context.session.thread_id
        user_session = cl.user_session
        thread_id = context.session.thread_id
        await cl.Message(content="正在恢复对话").send()
        graph = await TaskGraph().compile_graph()
        user_session.set("graph", graph)

        context.session.has_first_interaction = True
        if not graph:
            cl.Message(content="工作流初始化失败").send()
            raise ValueError("graph 未初始化")

        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        pre_state = await graph.aget_state(thread, subgraphs=True)
        LOG.info("()on_chat_resume %s", thread_id)

        all_steps = await curd_chat.get_steps_by_thread(thread_id)
        LOG.info("all_steps %s", all_steps)

    async def on_message(self, message: cl.Message):
        init_mtmai_http_context()
        try:
            user_session = cl.user_session
            thread_id = context.session.thread_id

            graph: CompiledGraph = user_session.get("graph")
            if not graph:
                cl.Message(content="工作流初始化失败").send()
                raise ValueError("graph 未初始化")

            thread: RunnableConfig = {
                "configurable": {
                    "thread_id": thread_id,
                    # 可以从指定检测点运行，以及分支
                    # "checkpoint_id": "xxxxx"
                }
            }

            all_checkpoints: list[StateSnapshot] = []
            async for state in graph.aget_state_history(thread):
                all_checkpoints.append(state)

            LOG.info("checkpoints: %d", len(all_checkpoints))

            pre_state: StateSnapshot = await graph.aget_state(thread, subgraphs=True)
            await graph.aupdate_state(
                thread,
                {
                    **pre_state.values,
                    "user_input": message.content,
                    "messages": [HumanMessage(content=message.content)],
                },
                as_node=HUMEN_INPUT_NODE,
            )
            await self.run_graph(thread)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\nDetailed traceback:\n{traceback.format_exc()}"
            LOG.error(error_message)
            await cl.Message(content=error_message).send()

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
                if thread_ui_state:
                    await context.emitter.emit(
                        "ui_state_upate",
                        jsonable_encoder(thread_ui_state),
                    )

            if kind == "on_tool_start":
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                    },
                )

            if kind == "on_tool_end":
                output = data.get("output")
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                        "output": jsonable_encoder(output),
                    },
                )

    # 旧代码，跟 lainlit 集成，但是，使用 ws 作为事件发送，大大增加了复杂性。对于兼容性非常不友好。
    # async def run_graph(
    #     self,
    #     thread: RunnableConfig,
    #     inputs=None,
    # ):
    #     # ############################################################################################
    #     # TODO: 对于非流式 http 的处理方式：
    #     #     本质就是，在本地用一个对象内部 使用流式更新状态，知道 graph 解释，再response 发送到前端。
    #     ##############################################################################################
    #     user_session = cl.user_session
    #     graph = user_session.get("graph")
    #     if not graph:
    #         raise ValueError("graph 未初始化")

    #     # 流式传输过程：
    #     # 1. 先发送一个消息，让前端立即显示ai消息占位，后续流程处理可随时更新这个消息，包括流式传输。
    #     # 2. 一旦整个流程结束，再次调用 .send()，触发消息的持久化。

    #     resp_msg = None

    #     async def prepare_message():
    #         nonlocal resp_msg
    #         resp_msg = cl.Message(content="")
    #         await resp_msg.send()

    #     async def stream_token(a: str):
    #         nonlocal resp_msg
    #         if not a:
    #             return
    #         if not resp_msg:
    #             await prepare_message()
    #         await resp_msg.stream_token(a)

    #     async def stream_finish():
    #         nonlocal resp_msg
    #         if resp_msg:
    #             await resp_msg.send()

    #     async for event in graph.astream_events(
    #         inputs,
    #         version="v2",
    #         config=thread,
    #         subgraphs=True,
    #     ):
    #         kind = event["event"]
    #         node_name = event["name"]
    #         data = event["data"]

    #         if not is_internal_node(node_name):
    #             if not is_skip_kind(kind):
    #                 LOG.info("[event] %s@%s", kind, node_name)

    #         if kind == "on_chat_model_stream":
    #             content = event["data"]["chunk"].content
    #             await stream_token(content)

    #         # if kind == "on_chat_model_end":
    #         #     output = data.get("output")
    #         #     if output:
    #         #         chat_output = output.content
    #         #         await resp_msg.send()

    #         if kind == "on_chain_start":
    #             LOG.info("on_chain_start %s:", node_name)
    #             output = data.get("output")
    #             if node_name == "__start__":
    #                 pass

    #         if kind == "on_chain_end":
    #             LOG.info("on_chain_end %s:", node_name)
    #             output = data.get("output")
    #             if node_name == "__start__":
    #                 pass
    #             if node_name in [HUMEN_INPUT_NODE, "articleGen", "entry"]:
    #                 human_ouput_message = output.get("human_ouput_message")
    #                 if human_ouput_message:
    #                     await stream_token(human_ouput_message)
    #                     elements = [
    #                         cl.Text(content="element 测试1"),
    #                         cl.Text(content="element 测试2"),
    #                         cl.Text(
    #                             name="simple_text",
    #                             content="element 测试3",
    #                             display="inline",
    #                         ),
    #                         cl.Text(
    #                             name="点击侧边栏打开文本",
    #                             content="element 测试4,侧边栏显示",
    #                             display="side",
    #                         ),
    #                     ]
    #                     await cl.Message(content="element 测试1", elements=elements).send()

    #         if node_name == "on_chat_start_node":
    #             thread_ui_state = output.get("thread_ui_state")
    #             if thread_ui_state:
    #                 await context.emitter.emit(
    #                     "ui_state_upate",
    #                     jsonable_encoder(thread_ui_state),
    #                 )

    #         if kind == "on_tool_start":
    #             await context.emitter.emit(
    #                 "logs",
    #                 {
    #                     "on": kind,
    #                     "node_name": node_name,
    #                 },
    #             )

    #         if kind == "on_tool_end":
    #             output = data.get("output")
    #             await context.emitter.emit(
    #                 "logs",
    #                 {
    #                     "on": kind,
    #                     "node_name": node_name,
    #                     "output": jsonable_encoder(output),
    #                 },
    #             )
    #         if node_name == "LangGraph":
    #             LOG.info("中止节点")
    #             if (
    #                 data
    #                 and (output := data.get("output"))
    #                 and (final_messages := output.get("messages"))
    #             ):
    #                 for message in final_messages:
    #                     message.pretty_print()
    #                 await context.emitter.emit(
    #                     "logs",
    #                     {
    #                         "on": "pause",
    #                         "node_name": node_name,
    #                         "output": json.dumps(jsonable_encoder(message)),
    #                     },
    #                 )
    #             await stream_finish()
