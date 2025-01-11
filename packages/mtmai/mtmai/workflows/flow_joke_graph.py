import uuid
from typing import cast

import structlog
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from mtmai.agents.ctx import init_mtmai_context, mtmai_context
from mtmai.agents.graphutils import is_internal_node, is_skip_kind
from mtmai.agents.joke_graph import joke_graph
from mtmai.core.coreutils import is_in_dev
from mtmai.worker import wfapp
from mtmaisdk.clients.rest.models import AgentNodeRunRequest
from mtmaisdk.context.context import Context

LOG = structlog.get_logger()


@wfapp.workflow(
    name="RunGraph", on_events=["graph:run"], input_validator=AgentNodeRunRequest
)
class PyJokeFlow:
    counter: int = 0
    graph: StateGraph | None

    @wfapp.step(timeout="20m", retries=2)
    async def graph_entry(self, hatctx: Context):
        self.counter += 1
        hatctx.log(f"counter: {self.counter}")
        init_mtmai_context(hatctx)
        input = cast(AgentNodeRunRequest, hatctx.workflow_input())

        thread_id = input.node_id
        if not thread_id:
            thread_id = str(uuid.uuid4())
        if not input.messages:
            input.messages = []

        self.graph = await joke_graph.JokeGraph().build_graph()
        graph = self.graph.compile(
            checkpointer=await mtmai_context.checkpointer(),
            interrupt_before=[
                # HUMEN_INPUT_NODE,
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
            save_to = "./.vol/joke_graph.png"
            with open(save_to, "wb") as f:
                f.write(image_data)

        stepId = uuid.UUID(hatctx.stepRunId)
        thread: RunnableConfig = {
            "run_id": stepId,
            "configurable": {
                "thread_id": thread_id,
                # 可以从指定检测点运行，以及分支
                # "checkpoint_id": "xxxxx"
            },
        }

        return await self.run_graph(
            graph,
            inputs=input,
            thread=thread,
        )

    async def run_graph(
        self, compiled_graph: CompiledGraph, inputs, thread: RunnableConfig
    ):
        async for event in compiled_graph.astream_events(
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
                    # mtmai_context.emit("logs", {"on": kind, "node_name": node_name})

            # if kind == "on_chat_model_stream":
            #     yield data

            if kind == "on_chain_start":
                LOG.info("on_chain_start %s:", node_name)
                # output = data.get("output")
                if node_name == "__start__":
                    pass

            if kind == "on_chain_end":
                LOG.info("on_chain_end %s:", node_name)
                output = data.get("output")
                if node_name == "__start__":
                    pass
                # if node_name in [HUMEN_INPUT_NODE, "articleGen", "entry"]:
                #     # human_ouput_message = output.get("human_ouput_message")
                #     # LOG.info("human_ouput_message %s", human_ouput_message)
                #     pass
            if node_name == "on_chat_start_node":
                # thread_ui_state = output.get("thread_ui_state")
                # if thread_ui_state:
                pass
                # await context.emitter.emit(
                #     "ui_state_upate",
                #     jsonable_encoder(thread_ui_state),
                # )

            if kind == "on_tool_start":
                pass

            if kind == "on_tool_end":
                pass
                # output = data.get("output")
