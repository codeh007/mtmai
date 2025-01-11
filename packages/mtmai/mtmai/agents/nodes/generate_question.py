from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda

from mtmai.agents.nodes.utils import swap_roles
from mtmai.core.logging import get_logger
from mtmai.llm.llm import get_fast_llm
from mtmai.models.graph_config import InterviewState

logger = get_logger()

gen_qn_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an experienced Wikipedia writer and want to edit a specific page. \
Besides your identity as a Wikipedia writer, you have a specific focus when researching the topic. \
Now, you are chatting with an expert to get information. Ask good questions to get more useful information.

When you have no more questions to ask, say "Thank you so much for your help!" to end the conversation.\
Please only ask one question at a time and don't ask what you have asked before.\
Your questions should be related to the topic you want to write.
Be comprehensive and curious, gaining as much unique insight from the expert as possible.\

Stay true to your specific perspective:

{persona}""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)


def tag_with_name(ai_message: AIMessage, name: str):
    ai_message.name = name
    return ai_message


class GenQuestionNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "gen_question"

    async def __call__(
        self,
        state: InterviewState,
        config: RunnableConfig,
    ):
        logger.info(f"进入 gen_question node: {state}")
        editor = state["editor"]
        gn_chain = (
            RunnableLambda(swap_roles).bind(name=editor.name)
            | gen_qn_prompt.partial(persona=editor.persona)
            | get_fast_llm()
            | RunnableLambda(tag_with_name).bind(name=editor.name)
        )
        result = await gn_chain.ainvoke(state)
        return {"messages": [result]}
