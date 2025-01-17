import uuid
from datetime import datetime
from textwrap import dedent

from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, START, StateGraph
from mtmaisdk.clients.rest.models import AssisantState

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.joke_graph.nodes.joke_writer_node import JokeWriterNode

from ....mtmaisdk.clients.rest.models.postiz_state import PostizState


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

    @staticmethod
    async def run(input: PostizState):
        graph = await PostizGraph().build_graph()
        thread_id = str(uuid.uuid4())
        if not thread_id:
            thread_id = str(uuid.uuid4())
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    dedent(
                        """Today is {time}, You are an assistant that gets a social media post or requests for a social media post.
                            You research should be on the most possible recent data.
                            You concat the text of the request together with an internet research based on the text.
                            {text}"""
                    ),
                ),
                # ("user", "{topic}")
            ]
        ).partial(time=datetime.now())

        ai_response = await mtmai_context.ainvoke_model(
            tpl=direct_gen_outline_prompt,
            inputs={"text": "todo user input text"},
        )

        return {"fresearch": "xxxxxxxxxxfresearchxxxxxxxxxxxx"}
