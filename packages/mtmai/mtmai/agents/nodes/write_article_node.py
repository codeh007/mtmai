from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.models.graph_config import InterviewState


writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Wikipedia author. Write the complete wiki article on {topic} using the following section drafts:\n\n"
            "{draft}\n\nStrictly follow Wikipedia format guidelines.",
        ),
        (
            "user",
            'Write the complete Wiki article using markdown format. Organize citations using footnotes like "[1]",'
            " avoiding duplicates in the footer. Include URLs in the footer.",
        ),
    ]
)


class WriteArticleNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "write_article"

    async def __call__(
        self,
        state: InterviewState,
        config: RunnableConfig,
    ):
        topic = state["topic"]
        sections = state["sections"]
        draft = "\n\n".join([section.as_str for section in sections])

        writer = writer_prompt | self.runnable | StrOutputParser()
        article = await writer.ainvoke({"topic": topic, "draft": draft})
        return {
            **state,
            "article": article,
        }
