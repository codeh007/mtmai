import logging
import operator
from collections.abc import Sequence
from functools import lru_cache
from typing import Annotated

from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger(__name__)


class BlogWriterAgentState(BaseModel):
    subjects: list[str] | None = None
    jokes: Annotated[Sequence[str], operator.add] | None = (
        None  # = Field(sa_column=Column(JSON))
    )
    best_selected_joke: str | None = None
    # messages: Annotated[list, add_messages] = Field(sa_column=Column(JSON))
    messages: list[dict] | None = None  # = Field(sa_column=Column(JSON))
    ask_human: bool = False


subjects_prompt = """Generate a comma separated list of between 2 and 5 examples related to: {topic}."""
joke_prompt = """Generate a joke about {subject}"""
best_joke_prompt = """Below are a bunch of jokes about {topic}. Select the best one! Return the ID of the best one.

{jokes}"""


class Subjects(BaseModel):
    subjects: list[str]


class Joke(BaseModel):
    joke: str


class BestJoke(BaseModel):
    id: int


class JokeState(BaseModel):
    subject: str


# This is the function we will use to generate the subjects of the jokes
def generate_topics(state: BlogWriterAgentState):
    llm = get_llm_chatbot_default()
    latest_message = state.messages[-1]
    prompt = subjects_prompt.format(topic=latest_message["content"])
    response = llm.with_structured_output(Subjects).invoke(prompt)
    state.subjects = response.subjects
    # return {"subjects": response.subjects}
    return state


# Here we generate a joke, given a subject
def generate_joke(state: JokeState):
    llm = get_llm_chatbot_default()
    prompt = joke_prompt.format(subject=state.subject)
    response = llm.with_structured_output(Joke).invoke(prompt)
    # state.jokes = [response.joke]
    return {"jokes": [response.joke]}
    # return state


# Here we define the logic to map out over the generated subjects
# We will use this an edge in the graph
def continue_to_jokes(state: BlogWriterAgentState):
    # We will return a list of `Send` objects
    # Each `Send` object consists of the name of a node in the graph
    # as well as the state to send to that node
    send_list = []
    for s in state.subjects:
        joke_state = JokeState(
            subject=s,
        )
        send_list.append(Send("generate_joke", joke_state))
    # return [Send("generate_joke", ) for JokeAgentState(subjects=s) in state.subjects]
    return send_list


# Here we will judge the best joke
def best_joke(state: BlogWriterAgentState):
    llm = get_llm_chatbot_default()

    jokes = "\n\n".join(state.jokes)
    latest_message = state.messages[-1]

    prompt = best_joke_prompt.format(topic=latest_message["content"], jokes=jokes)
    response = llm.with_structured_output(BestJoke).invoke(prompt)

    idx = response.id

    # Ensure idx is within the bounds of the jokes list
    if idx >= len(state.jokes):
        idx = len(state.jokes) - 1

    return {"best_selected_joke": state.jokes[idx]}


@lru_cache
def get_workflow() -> CompiledStateGraph:
    graph = StateGraph(BlogWriterAgentState)
    graph.add_node("generate_topics", generate_topics)
    graph.add_node("generate_joke", generate_joke)
    graph.add_node("best_joke", best_joke)
    graph.add_edge(START, "generate_topics")
    graph.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
    graph.add_edge("generate_joke", "best_joke")
    graph.add_edge("best_joke", END)
    app = graph.compile()
    return app
