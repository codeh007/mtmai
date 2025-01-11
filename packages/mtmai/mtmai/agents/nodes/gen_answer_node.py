import asyncio
import json

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field

from mtmai.agents.nodes.utils import swap_roles
from mtmai.agents.retrivers.web_search import search_engine
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import InterviewState

logger = get_logger()


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


class Queries(BaseModel):
    queries: list[str] = Field(
        description="Comprehensive list of search engine queries to answer the user's questions.",
    )


class GenAnswerNode:
    def __init__(
        self,
        runnable: Runnable,
        name: str = "Subject_Matter_Expert",
        max_str_len: int = 15000,
    ):
        self.runnable = runnable
        self.name = name
        self.max_str_len = max_str_len

    def node_name(self):
        return "gen_answer"

    async def __call__(
        self,
        state: InterviewState,
        config: RunnableConfig,
    ):
        logger.info(f"进入 gen_answer node: {state}")
        swapped_state = swap_roles(state, self.name)  # Convert all other AI messages

        # gen_queries_chain = gen_queries_prompt | self.runnable.with_structured_output(
        #     Queries, include_raw=True
        # ).with_retry(stop_after_attempt=3)

        # queries = await gen_queries_chain.ainvoke(swapped_state)
        queries = await self.gen_queries(swapped_state, self.runnable)
        parsed_queries = queries["parsed"]
        if not parsed_queries:
            logger.warning("生成搜索查询失败")
            return {"error": " gen_answer 没有生成查询"}
        queries_input = parsed_queries.queries
        query_results = await search_engine.abatch(
            queries_input, config, return_exceptions=True
        )
        successful_results = [
            res for res in query_results if not isinstance(res, Exception)
        ]
        all_query_results = {
            res["url"]: res["content"]
            for results in successful_results
            for res in results
        }
        # We could be more precise about handling max token length if we wanted to here
        dumped = json.dumps(all_query_results)[: self.max_str_len]
        ai_message: AIMessage = queries["raw"]
        tool_call = queries["raw"].additional_kwargs["tool_calls"][0]
        tool_id = tool_call["id"]
        tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)
        swapped_state["messages"].extend([ai_message, tool_message])
        # Only update the shared state with the final answer to avoid
        # polluting the dialogue history with intermediate messages

        llm = self.runnable
        # gen_answer_chain = gen_answer_prompt | llm.with_structured_output(
        #     AnswerWithCitations, include_raw=True
        # ).with_config(run_name="GenerateAnswer").with_retry(stop_after_attempt=5)
        # generated = await gen_answer_chain.ainvoke(swapped_state)
        generated = await self.gen_answer(swapped_state, llm)
        cited_urls = set(generated["parsed"].cited_urls)
        if cited_urls:
            # Save the retrieved information to a the shared state for future reference
            cited_references = {
                k: v for k, v in all_query_results.items() if k in cited_urls
            }
        else:
            logger.warning("没有生成引用")
            cited_references = {}
        formatted_message = AIMessage(
            name=self.name, content=generated["parsed"].as_str
        )

        logger.info(f"gen_answer node 结束: {self.name}")
        return {"messages": [formatted_message], "references": cited_references}

    async def gen_answer(self, swapped_state, llm: Runnable):
        gen_answer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert who can use information effectively. You are chatting with a Wikipedia writer who wants\
        to write a Wikipedia page on the topic you know. You have gathered the related information and will now use the information to form a response.

        Make your response as informative as possible and make sure every sentence is supported by the gathered information.
        Each response must be backed up by a citation from a reliable source, formatted as a footnote, reproducing the URLS after your response.""",
                ),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )

        # parser = PydanticOutputParser(pydantic_object=AnswerWithCitations)
        # retry_parser = RetryOutputParser.from_llm(parser=parser, llm=llm)

        gen_answer_chain = gen_answer_prompt | llm.with_structured_output(
            AnswerWithCitations, include_raw=True
        ).with_config(run_name="GenerateAnswer").with_retry(stop_after_attempt=5)

        max_retries = 5
        for attempt in range(max_retries):
            try:
                generated = await gen_answer_chain.ainvoke(swapped_state)
                if generated is None or not isinstance(
                    generated.get("parsed"), AnswerWithCitations
                ):
                    raise ValueError("Invalid response format")
                return generated
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Returning error.")
                    return {
                        "error": "Failed to generate a valid response after multiple attempts"
                    }
                await asyncio.sleep(20)

    async def gen_queries(self, swapped_state, llm: Runnable):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                gen_queries_prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are a helpful research assistant. Query the search engine to answer the user's questions.",
                        ),
                        MessagesPlaceholder(variable_name="messages", optional=True),
                    ]
                )
                gen_queries_chain = (
                    gen_queries_prompt
                    | self.runnable.with_structured_output(
                        Queries, include_raw=True
                    ).with_retry(stop_after_attempt=5)
                )

                queries = await gen_queries_chain.ainvoke(swapped_state)

                if queries is None or not isinstance(queries.get("parsed"), Queries):
                    raise ValueError("生成搜索查询失败")
                return queries
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Raising the last exception.")
                    raise
                await asyncio.sleep(20)
