from langgraph.graph import END, START, StateGraph
from mtmaisdk.clients.rest.models import AssisantState

from mtmai.agents.joke_graph.nodes.joke_writer_node import JokeWriterNode


class JokeGraph:
    @property
    def name(self):
        return "jokeGraph"

    @property
    def description(self):
        return "笑话生成器(用于测试)"

    async def build_graph(self):
        builder = StateGraph(AssisantState)

        builder.add_node("joke_writer", JokeWriterNode())
        builder.add_edge(START, "joke_writer")
        builder.add_edge("joke_writer", END)

        return builder
