import json
import uuid

import orjson
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph.message import AnyMessage
from pydantic import BaseModel, Field

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.tools.web_search import search_engine
from mtmai.core.logging import get_logger
from mtmai.llm.llm import get_fast_llm
from mtmai.models.graph_config import Editor, InterviewState

logger = get_logger()

max_str_len: int = 15000


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state.messages:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.model_dump(exclude={"type"}))
        converted.append(message)
    return InterviewState(
        messages=converted,
        references=state.references,
        editor=state.editor,
    )


def tag_with_name(ai_message: AIMessage, name: str):
    ai_message.name = name
    return ai_message


class QaNodeRequest(BaseModel):
    topic: str
    editor: Editor
    max_turns: int = 5


class QaNodeResult(BaseModel):
    editor: Editor
    messages: list[AIMessage]

    def format_conversation(self):
        messages = self.messages
        convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
        return f"Conversation with {self.editor.name}\n\n" + convo


async def node_qa(req: QaNodeRequest) -> QaNodeResult:
    """
    以问答的方式发起多轮对话。
    一般应用场景是:
        1. 给定领域专家名称，提问者根据给定目的和主题发起多轮提问
    """
    topic = req.topic
    editor = req.editor

    # TODO: 提示词，需要完善
    init_messages = [
        AIMessage(
            content=f"So you said you were writing an article on {topic}?",
            name="Subject_Matter_Expert",
        )
    ]
    state = InterviewState(topic=topic, editor=editor, messages=init_messages)
    # ctx = get_mtmai_ctx()

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

    llm = get_fast_llm()

    max_turns = req.max_turns
    for i in range(max_turns):
        # Step 1: Swap roles
        swapped_state = swap_roles(state, editor.name)

        # Step 2: Generate prompt with persona
        prompt = gen_qn_prompt.format(
            persona=editor.persona, messages=swapped_state.messages
        )

        # Step 3: Call the language model
        llm_response = await llm.ainvoke(prompt)

        # Step 4: Tag the response with the editor's name
        result = tag_with_name(llm_response, editor.name)

        state.messages.append(result)

        # 专家回答开始 ==============================================================================
        name = "Subject_Matter_Expert"
        swapped_state = swap_roles(state, name)  # Convert all other AI messages
        queries = await _gen_queries(swapped_state.messages)
        if not queries:
            logger.warning("生成搜索查询失败")
            return {"error": " gen_answer 没有生成查询"}
        # queries_input = parsed_queries.queries
        query_results = await search_engine.abatch(queries.queries)
        successful_results = [
            res for res in query_results if not isinstance(res, Exception)
        ]
        all_query_results = {
            res["url"]: res["content"]
            for results in successful_results
            for res in results
        }
        # We could be more precise about handling max token length if we wanted to here
        # Construct AI message with tool call
        tool_id = str(uuid.uuid4())[:10]
        tool_call = {
            "id": tool_id,
            "type": "function",
            "function": {
                "name": "search",
                "arguments": json.dumps({"queries": queries.queries}),
            },
        }
        ai_message = AIMessage(
            content="Searching for information...",
            additional_kwargs={"tool_calls": [tool_call]},
        )

        # Construct tool message with search results
        dumped = json.dumps(all_query_results)[:max_str_len]
        tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)

        # Add both messages to the state
        state.messages.extend([ai_message, tool_message])

        answer: AnswerWithCitations = await _gen_answer(state.messages)
        cited_urls = set(answer.cited_urls)
        if cited_urls:
            # Save the retrieved information to a the shared state for future reference
            cited_references = {
                k: v for k, v in all_query_results.items() if k in cited_urls
            }
        else:
            logger.warning("没有生成引用")
            cited_references = {}
        formatted_message = AIMessage(name=name, content=answer.answer)

        data2 = {"messages": [formatted_message], "references": cited_references}

    return QaNodeResult(editor=state.editor, messages=init_messages)


class Queries(BaseModel):
    queries: list[str] = Field(
        description="Comprehensive list of search engine queries to answer the user's questions.",
    )


async def _gen_queries(messages: list[AnyMessage]):
    parser = PydanticOutputParser(pydantic_object=Queries)
    gen_queries_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful research assistant. Query the search engine to answer the user's questions."
                "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                "\n- Use double quotes for all strings"
                "\n- Ensure all keys and values are properly enclosed"
                "\n- Do not include any text outside of the JSON object"
                "\n- Strictly adhere to the following JSON schema:"
                "\n{format_instructions}"
                "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
            ),
            MessagesPlaceholder(variable_name="messages", optional=False),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions(),
        messages=messages,
    )
    ai_response = await mtmai_context.call_model_chat(gen_queries_prompt, {})
    return Queries.model_validate(
        orjson.loads(mtmai_context.repair_json(ai_response.content))
    )


class AnswerWithCitations(BaseModel):
    answer: str = Field(
        description="Comprehensive answer to the user's question with citations.",
    )
    cited_urls: list[str] = Field(
        description="List of urls cited in the answer.",
    )

    @property
    def as_str(self) -> str:
        return f"{self.answer}\n\nCitations:\n\n" + "\n".join(
            f"[{i+1}]: {url}" for i, url in enumerate(self.cited_urls)
        )


async def _gen_answer(messages: list[AnyMessage]):
    parser = PydanticOutputParser(pydantic_object=AnswerWithCitations)
    gen_answer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert who can use information effectively. You are chatting with a Wikipedia writer who wants"
                "to write a Wikipedia page on the topic you know. You have gathered the related information and will now use the information to form a response."
                "Make your response as informative as possible and make sure every sentence is supported by the gathered information."
                "Each response must be backed up by a citation from a reliable source, formatted as a footnote, reproducing the URLS after your response."
                "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                "\n- Use double quotes for all strings"
                "\n- Ensure all keys and values are properly enclosed"
                "\n- Do not include any text outside of the JSON object"
                "\n- Strictly adhere to the following JSON schema:"
                "\n{format_instructions}"
                "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
            ),
            MessagesPlaceholder(variable_name="messages", optional=False),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions(),
    )

    ai_response = await mtmai_context.call_model_chat(
        gen_answer_prompt,
        {
            "messages": messages,
        },
    )
    return AnswerWithCitations.model_validate(
        orjson.loads(mtmai_context.repair_json(ai_response.content))
    )
