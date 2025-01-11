from langchain_core.prompts import ChatPromptTemplate

from mtmai.core.logging import get_logger
from mtmai.llm.llm import get_llm_long_context_default
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.runnables import chain as as_runnable
from langchain_core.runnables import Runnable, RunnableConfig

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from mtmai.agents.retrivers.web_search import search_engine
from mtmai.core.logging import get_logger

from mtmai.llm.llm import get_fast_llm
from mtmai.models.graph_config import Outline, ResearchState

logger = get_logger()

def format_conversation(interview_state):
    messages = interview_state["messages"]
    convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
    return f'Conversation with {interview_state["editor"].name}\n\n' + convo


refine_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Wikipedia writer. You have gathered information from experts and search engines. Now, you are refining the outline of the Wikipedia page. \
You need to make sure that the outline is comprehensive and specific. \
Topic you are writing about: {topic}

Old outline:

{old_outline}""",
        ),
        (
            "user",
            "Refine the outline based on your conversations with subject-matter experts:\n\nConversations:\n\n{conversations}\n\nWrite the refined Wikipedia outline:",
        ),
    ]
)



class RefineOutlineNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "refine_outline"

    async def __call__(self, state: ResearchState, config: RunnableConfig):
        """根据前面多个专家给出的观点，重新编辑大纲"""
        logger.info(f"进入 refine_outline node: {state}")
        convos = "\n\n".join(
            [
                format_conversation(interview_state)
                for interview_state in state["interview_results"]
            ]
        )

        # Using turbo preview since the context can get quite long
        refine_outline_chain = (
            refine_outline_prompt
            | get_llm_long_context_default().with_structured_output(Outline)
        )
        updated_outline = await refine_outline_chain.ainvoke(
            {
                "topic": state["topic"],
                "old_outline": state["outline"].as_str,
                "conversations": convos,
            }
        )
        return {**state, "outline": updated_outline}
