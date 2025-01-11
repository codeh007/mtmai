import uuid

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.message import AnyMessage

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.opencanvas.nodes.generateArtifact import GenerateArtifactNode
from mtmai.agents.opencanvas.nodes.generatePath import GeneratePath, routeGeneratePath
from mtmai.agents.opencanvas.nodes.respondToQuery import RespondToQueryNode
from mtmai.agents.opencanvas.opencanvas_state import OpenCanvasState
from mtmai.agents.sitegen_graph.assistant_site import SiteAssistantNode
from mtmai.core.logging import get_logger
from mtmai.mtlibs import aisdk

logger = get_logger()


class OpenCanvasGraph:
    def __init__(self):
        pass

    async def build_graph(self):
        wf = StateGraph(OpenCanvasState)
        wf.add_node("generatePath", GeneratePath())
        wf.set_entry_point("generatePath")

        wf.add_node("siteAssistant", SiteAssistantNode())
        wf.add_conditional_edges(
            "generatePath",
            routeGeneratePath,
            [
                "siteAssistant",
                # "updateArtifact",
                # "rewriteArtifactTheme",
                # "rewriteCodeArtifactTheme",
                "respondToQuery",
                "generateArtifact",
                # "rewriteArtifact",
            ],
        )
        wf.add_node("respondToQuery", RespondToQueryNode())
        wf.add_node("generateArtifact", GenerateArtifactNode())
        # wf.add_edge("respondToQuery", "RespondToQueryNode")

        return wf

    async def compile_graph(self):
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            # interrupt_before=[
            #     "human_chat",
            #     # "update_flight_sensitive_tools",
            #     # "develop_sensitive_tools",
            #     # "book_car_rental_sensitive_tools",
            #     # "book_hotel_sensitive_tools",
            #     # "book_excursion_sensitive_tools",
            # ],
            debug=True,
        )

        image_data = graph.get_graph(xray=1).draw_mermaid_png()
        save_to = "./.vol/graph-opencanvas.png"
        with open(save_to, "wb") as f:
            f.write(image_data)
        return graph

    async def run_graph(
        self,
        messages: list[AnyMessage] = [],
        thread_id: str | None = None,
        user_id: str | None = None,
        params: dict | None = None,
    ):
        graph = await self.compile_graph()
        inputs = {
            "messages": messages,
            "userId": user_id,
            "params": params,
        }

        if not thread_id:
            thread_id = str(uuid.uuid4())
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
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

            yield aisdk.data(event)
            # if not is_internal_node(node_name):
            #     if not is_skip_kind(kind):
            #         logger.info("[event] %s@%s", kind, node_name)

            # if kind == "on_chat_model_stream":
            #     content = event["data"]["chunk"].content
            #     if content:
            #         yield aisdk.text(content)
