import asyncio
from textwrap import dedent

import orjson
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field

# import mtmai.chainlit as cl
from mtmai.agents.ctx import mtmai_context
from mtmai.agents.tools.wikipedia import MtmTopicDocRetriever
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import Outline, Perspectives, ResearchState

logger = get_logger()


class RelatedSubjects(BaseModel):
    topics: list[str] = Field(
        description="Comprehensive list of related subjects as background research.",
    )


class InitializeResearchNode:
    state: ResearchState = None

    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "initialize_research"

    async def __call__(self, state: ResearchState, config: RunnableConfig):
        logger.info("进入 initialize_research node")
        topic = state["topic"]
        self.state = state

        try:
            outline_task = asyncio.create_task(self.init_outline(topic))
            subjects_task = asyncio.create_task(self.survey_subjects(topic))

            outline, subjects = await asyncio.gather(outline_task, subjects_task)

            return {
                **state,
                "outline": outline,  # 初始大纲，后续流程会对这个大纲进行改进
                "editors": subjects.editors,
            }
        except Exception as e:
            import traceback

            error_message = f"Error in initialize_research: {str(e)}\n\nStacktrace:\n{traceback.format_exc()}"
            logger.error(error_message)
            return {**state, "error": error_message}

    @cl.step
    async def init_outline(self, topic: str):
        """初始化大纲"""
        # ctx = get_mtmai_ctx()
        parser = PydanticOutputParser(pydantic_object=Outline)
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."
                    "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                    "\n- Use double quotes for all strings"
                    "\n- Ensure all keys and values are properly enclosed"
                    "\n- Do not include any text outside of the JSON object"
                    "\n- Strictly adhere to the following JSON schema:"
                    "\n{format_instructions}"
                    "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
                ),
                ("user", "{topic}"),
            ]
        ).partial(format_instructions=parser.get_format_instructions())
        ai_response = await mtmai_context.call_model_chat(
            direct_gen_outline_prompt, {"topic": topic}
        )

        loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
        outline: Outline = Outline.model_validate(loaded_data)
        return outline

    async def survey_subjects(self, topic: str):
        """获取相关主题"""
        parser = PydanticOutputParser(pydantic_object=RelatedSubjects)
        gen_related_topics_prompt = ChatPromptTemplate.from_template(
            template=dedent("""I'm writing a Wikipedia page for a topic mentioned below. Please identify and recommend some Wikipedia pages on closely related subjects. I'm looking for examples that provide insights into interesting aspects commonly associated with this topic, or examples that help me understand the typical content and structure included in Wikipedia pages for similar topics.
            Please list the as many subjects and urls as you can.
            "[Requirements]"
            "- No explanations, greetings, or other unnecessary words. Output only in strict JSON data format"
            ""
            {format_instructions}
            Topic of interest: {topic}
            """),
            # input_variables=["topic"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        ai_response = await mtmai_context.call_model_chat(
            gen_related_topics_prompt, {"topic": topic}
        )
        related_subjects = parser.parse(ai_response.content)
        examples = await MtmTopicDocRetriever().retrive(related_subjects.topics)

        ####################################################################################################
        perspectives_parser = PydanticOutputParser(pydantic_object=Perspectives)
        gen_perspectives_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You need to select a diverse (and distinct) group of Wikipedia editors who will work together to create a comprehensive article on the topic. Each of them represents a different perspective, role, or affiliation related to this topic."
                    "You can use other Wikipedia pages of related topics for inspiration. For each editor, add a description of what they will focus on."
                    "[Requirements]"
                    "- No explanations, greetings, or other unnecessary words. Output only in strict JSON data format"
                    "{format_instructions}"
                    "Wiki page outlines of related topics for inspiration:"
                    "{examples}",
                ),
                ("user", "Topic of interest: {topic}"),
            ]
        ).partial(format_instructions=perspectives_parser.get_format_instructions())
        ai_response = await mtmai_context.call_model_chat(
            gen_perspectives_prompt, {"topic": topic, "examples": examples}
        )
        loaded_data = orjson.loads(mtmai_context.repair_json(ai_response.content))
        perspectives = Perspectives.model_validate(loaded_data)
        return perspectives
