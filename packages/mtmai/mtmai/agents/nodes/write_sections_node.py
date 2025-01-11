from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.ctx import get_mtmai_ctx

from mtmai.core.logging import get_logger
from mtmai.models.graph_config import InterviewState, Outline, ResearchState, WikiSection

logger = get_logger()

section_writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Wikipedia writer. Complete your assigned WikiSection from the following outline:\n\n"
            "{outline}\n\nCite your sources, using the following references:\n\n<Documents>\n{docs}\n<Documents>",
        ),
        ("user", "Write the full WikiSection for the {section} section."),
    ]
)


def format_conversation(interview_state):
    messages = interview_state["messages"]
    convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
    return f'Conversation with {interview_state["editor"].name}\n\n' + convo


class WriteSectionsNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "gen_question"

    async def __call__(
        self,
        state: InterviewState,
        config: RunnableConfig,
    ):
        """Write the individual sections of the article"""
        outline = state["outline"]

        refined_outline = await self.get_refine_outline(state)

        section_writer = await self.get_section_writer(state)

        enable_batch = False
        if enable_batch:
            sections = await section_writer.abatch(
                [
                    {
                        "outline": refined_outline,
                        "section": section.section_title,
                        "topic": state["topic"],
                    }
                    for section in outline.sections
                ]
            )
        else:
            sections = []
            for section in outline.sections:
                sections.append(
                    await section_writer.ainvoke(
                        {
                            "outline": refined_outline,
                            "section": section.section_title,
                            "topic": state["topic"],
                        }
                    )
                )
        return {
            **state,
            "sections": sections,
        }

    async def get_section_writer(self, state: ResearchState):
        ctx = get_mtmai_ctx()
        vs = ctx.vectorstore
        retriever = vs.as_retriever(k=10)

        async def retrieve(inputs: dict):
            import asyncio

            from tenacity import retry, stop_after_attempt, wait_fixed

            @retry(stop=stop_after_attempt(6), wait=wait_fixed(10))
            async def retrieve_with_retry(retriever, topic, section):
                return await retriever.ainvoke(topic + ": " + section)

            try:
                docs = await retrieve_with_retry(
                    retriever, inputs["topic"], inputs["section"]
                )
                formatted = "\n".join(
                    [
                        f'<Document href="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
                        for doc in docs
                    ]
                )
                return {"docs": formatted, **inputs}
            except Exception as e:
                logger.error(f"Failed to retrieve documents after 6 attempts: {str(e)}")
                return {"docs": "", **inputs}

        section_writer = (
            retrieve
            | section_writer_prompt
            | self.runnable.with_structured_output(WikiSection).with_retry(
                stop_after_attempt=3
            )
        )
        return section_writer

    async def get_refine_outline(self, state: ResearchState):
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

        # Using turbo preview since the context can get quite long
        refine_outline_chain = (
            refine_outline_prompt | self.runnable.with_structured_output(Outline)
        )

        convos = "\n\n".join(
            [
                format_conversation(interview_state)
                for interview_state in state.get("interview_results", [])
            ]
        )

        updated_outline = await refine_outline_chain.ainvoke(
            {
                "topic": state["topic"],
                "old_outline": state["outline"],
                "conversations": convos,
            }
        )
        return {**state, "outline": updated_outline}
