from langgraph.graph import END, START, StateGraph
from mtmai.agents.joke_graph.nodes.joke_writer_node import JokeWriterNode

from mtmaisdk.clients.rest.models import AssisantState


class PostizGraph:
    @property
    def name(self):
        return "postizGraph"

    @property
    def description(self):
        return "社交媒体贴文生成器"

    async def build_graph(self):
        builder = StateGraph(AssisantState)

        builder.add_node("joke_writer", JokeWriterNode())
        builder.add_edge(START, "joke_writer")
        builder.add_edge("joke_writer", END)

        return builder
