import uuid

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from mtmai.agents.joke_graph.nodes.joke_writer_node import JokeWriterNode
from mtmai.agents.nodes.initialize_research_node import InitializeResearchNode
from mtmaisdk.clients.rest.models.postiz_state import PostizState

from .static import PostizGraphState

# from langgraph.checkpoint.memory import MemorySaver


class PostizGraph:
    @property
    def name(self):
        return "postizGraph"

    @property
    def description(self):
        return "社交媒体贴文生成器"

    async def build_graph(self):
        builder = StateGraph(PostizGraphState)
        builder.add_node("init_research", InitializeResearchNode())

        builder.add_node("joke_writer", JokeWriterNode())
        builder.add_edge(START, "joke_writer")
        builder.add_edge("joke_writer", END)

        return builder

    @staticmethod
    async def run(input: PostizState, thread_id: str | None = None):
        builded_graph = await PostizGraph().build_graph()

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
