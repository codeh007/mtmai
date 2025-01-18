from textwrap import dedent

import orjson
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.nodes.initialize_research_node import RelatedSubjects
from mtmai.agents.nodes.qa_node import QaNodeResult
from mtmai.agents.tools.wikipedia import MtmTopicDocRetriever
from mtmai.core.logging import get_logger
from mtmai.llm.llm import get_llm_long_context_default
from mtmai.models.graph_config import Outline, Perspectives, Section, WikiSection

logger = get_logger()


# @cl.step
async def init_outline(topic: str):
    """初始化大纲"""
    # ctx = get_mtmai_ctx()
    current_step = cl.context.current_step
    logger.info(f"current_step: {current_step}")

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
            ("user", "topic is: {topic}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    ai_response = await mtmai_context.call_model_chat(
        direct_gen_outline_prompt, {"topic": topic}
    )

    loaded_data = orjson.loads(mtmai_context.repair_json(ai_response.content))
    outline: Outline = Outline.model_validate(loaded_data)
    return outline


@cl.step(name="大纲草稿", type="llm")
async def init_outline_v2(topic: str):
    """初始化大纲"""
    current_step = cl.context.current_step
    logger.info(f"current_step: {current_step}")

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
            ("user", "topic is: {topic}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    # ai_response = await ctx.astream(direct_gen_outline_prompt, {"topic": topic})
    messages = await direct_gen_outline_prompt.ainvoke({"topic": topic})
    llm_chat = mtmai_context.graph_config.llms.get("chat")

    llm_inst = ChatOpenAI(
        base_url=llm_chat.base_url,
        api_key=llm_chat.api_key,
        model=llm_chat.model,
        temperature=llm_chat.temperature,
        max_tokens=llm_chat.max_tokens,
    )

    llm_chain = llm_inst.with_retry(stop_after_attempt=5)
    llm_chain = llm_chain.bind(response_format={"type": "json_object"})

    current_step = cl.context.current_step
    async for event in llm_chain.astream_events(messages, version="v2"):
        kind = event["event"]
        node_name = event["name"]
        # logger.info(f"kind: {kind}, node_name: {node_name}")
        data = event["data"]
        if kind == "on_chat_model_stream":
            content = data["chunk"].content
            if content:
                # yield aisdk.text(content)
                await current_step.stream_token(content)

        if kind == "on_chat_model_end":
            output = data.get("output")
            if output:
                chat_output = output.content
                current_step.output = "大语言模型输出：" + chat_output
        if kind == "on_llm_end":
            pass
        # if chunk.content:
        #     print(chunk.content)
        #     await current_step.stream_token(chunk.content)
    # loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
    # outline: Outline = Outline.model_validate(loaded_data)
    return ""


async def init_outline_v3(topic: str):
    """初始化大纲"""
    async with cl.Step(name="初始化大纲(v3)", type="llm") as step:
        current_step = cl.context.current_step
        logger.info(f"current_step: {current_step}")

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
                ("user", "topic is: {topic}"),
            ]
        ).partial(format_instructions=parser.get_format_instructions())
        # ai_response = await ctx.astream(direct_gen_outline_prompt, {"topic": topic})
        messages = await direct_gen_outline_prompt.ainvoke({"topic": topic})
        llm_chat = mtmai_context.graph_config.llms.get("chat")

        llm_inst = ChatOpenAI(
            base_url=llm_chat.base_url,
            api_key=llm_chat.api_key,
            model=llm_chat.model,
            temperature=llm_chat.temperature,
            max_tokens=llm_chat.max_tokens,
        )

        llm_chain = llm_inst.with_retry(stop_after_attempt=5)
        llm_chain = llm_chain.bind(response_format={"type": "json_object"})

        current_step = cl.context.current_step

        async for event in llm_chain.astream_events(messages, version="v2"):
            kind = event["event"]
            node_name = event["name"]
            # logger.info(f"kind: {kind}, node_name: {node_name}")
            data = event["data"]
            if kind == "on_chat_model_stream":
                content = data["chunk"].content
                if content:
                    # yield aisdk.text(content)
                    await current_step.stream_token(content)

            if kind == "on_chat_model_end":
                output = data.get("output")
                if output:
                    chat_output = output.content
            if kind == "on_llm_end":
                pass
            # if chunk.content:
            #     print(chunk.content)
            #     await current_step.stream_token(chunk.content)
        loaded_data = orjson.loads(mtmai_context.repair_json(chat_output))
        outline: Outline = Outline.model_validate(loaded_data)
        current_step.output = chat_output

        return outline


async def node_survey_subjects(topic: str):
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


class RefineOutlineNodeRequest(BaseModel):
    topic: str
    old_outline: Outline
    qa_results: list[QaNodeResult]


class RefineOutlineNodeResponse(BaseModel):
    outline: Outline


async def node_refine_outline(state: RefineOutlineNodeRequest):
    """根据前面多个专家给出的观点，重新编辑大纲"""
    logger.info(f"进入 refine_outline node: {state}")

    def format_conversation(qa_result: QaNodeResult):
        messages = qa_result.messages
        convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
        return f"Conversation with {qa_result.editor.name}\n\n" + convo

    refine_outline_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a Wikipedia writer. You have gathered information from experts and search engines. Now, you are refining the outline of the Wikipedia page. \
    You need to make sure that the outline is comprehensive and specific. \
    Topic you are writing about: {topic}

    outline:

    {outline}""",
            ),
            (
                "user",
                "Refine the outline based on your conversations with subject-matter experts:\n\nConversations:\n\n{conversations}\n\nWrite the refined Wikipedia outline:",
            ),
        ]
    )

    # Using turbo preview since the context can get quite long
    refine_outline_chain = (
        refine_outline_prompt
        | get_llm_long_context_default().with_structured_output(Outline)
    )
    updated_outline = await refine_outline_chain.ainvoke(
        {
            "topic": state.topic,
            "outline": state.old_outline,
            "conversations": "\n\n".join(
                format_conversation(qa_result) for qa_result in state.qa_results
            ),
        }
    )
    return RefineOutlineNodeResponse(outline=updated_outline)


class NodeSectionWriterRequest(BaseModel):
    outline: Outline
    section: Section
    topic: str


async def node_section_writer(state: NodeSectionWriterRequest):
    """
    独立编写一个章节
    Write the individual sections of the article
    """

    outline = state.outline
    section = state.section
    topic = state.topic
    vs = mtmai_context.vectorstore
    retriever = vs.as_retriever(k=10)

    async def retrieve(inputs: dict):
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

    perspectives_parser = PydanticOutputParser(pydantic_object=WikiSection)
    section_writer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert Wikipedia writer. Complete your assigned WikiSection from the following outline:\n\n"
                "{format_instructions}"
                "{outline}\n\nCite your sources, using the following references:\n\n<Documents>\n{docs}\n<Documents>",
            ),
            ("user", "Write the full WikiSection for the {section} section."),
        ]
    ).partial(format_instructions=perspectives_parser.get_format_instructions())

    ai_response = await mtmai_context.call_model_chat(
        section_writer_prompt,
        {"outline": outline, "section": section, "topic": state.topic},
    )
    loaded_data = orjson.loads(mtmai_context.repair_json(ai_response.content))
    perspectives = Perspectives.model_validate(loaded_data)
    return perspectives

    # sections = []
    # for section in outline.sections:
    #     sections.append(
    #         await section_writer.ainvoke(
    #             {
    #                 "outline": refined_outline,
    #                 "section": section.section_title,
    #                 "topic": state["topic"],
    #             }
    #         )
    #     )
