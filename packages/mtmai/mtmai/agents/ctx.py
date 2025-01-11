import asyncio
import json
import os
from contextvars import ContextVar
from functools import lru_cache
from typing import Type

import httpx
import orjson
import structlog
from attr import make_class
# from crewai import LLM
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import StructuredTool
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres.aio import (AsyncPostgresSaver,
                                               BasePostgresSaver)
from lazify import LazyProxy
from mtmai.agents import utils
from mtmai.agents.graphutils import ensure_valid_llm_response_v2
from mtmai.core.config import settings
from mtmai.models.graph_config import GraphConfig
from mtmai.mtlibs import yaml
from mtmaisdk import Context as HatchetContext
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel

LOG = structlog.get_logger()

context_var: ContextVar["AgentContext"] = ContextVar("mtmai")


class LoggingTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        response = await super().handle_async_request(request)
        # 提示： 不要读取 body，因为一般 是stream，读取了会破环状态
        LOG.info(
            f"OPENAI Response: {response.status_code}\n {request.url}\nreq:\n{str(request.content)}\n"
        )
        return response


@lru_cache(maxsize=1)
def get_graph_config() -> GraphConfig:
    if not os.path.exists(settings.graph_config_path):
        raise Exception(f"未找到graph_config配置文件: {settings.graph_config_path}")
    config_dict = yaml.load_yaml_file(settings.graph_config_path) or {}

    sub = config_dict.get("mtmai_config")
    return GraphConfig.model_validate(sub)


class AgentContext:
    tenant_id: str | None
    user_id: str | None
    thread_id: str | None
    cache_checkpointer: BasePostgresSaver | None

    def __init__(
        self,
        *,
        thread_id: str | None = None,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ):
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.thread_id = thread_id
        # self.httpx_session: httpx.Client = None
        # self.db: Engine = db_engine
        # self.session: Session = Session(db_engine)
        # embedding = get_default_embeddings()

        # self.vectorstore = MtmDocStore(session=Session(db_engine), embedding=embedding)
        # self.kvstore = MtmKvStore(db_engine)

        self.graph_config = get_graph_config()
        self._mq = None
        # self.memMq = MemoryMQ()
        self._thread_id = thread_id

    def set_hatch_context(self, ctx: HatchetContext):
        self.hatchet_ctx = ctx

    def log(self, lineformat, **kw_args):
        if self.hatchet_ctx:
            self.hatchet_ctx.log(
                lineformat,
                kw_args,
            )
        else:
            LOG.info(lineformat, kw_args)

    def retrive_graph_config(self):
        return self.graph_config

    # def load_doc(self):
    #     return self.vectorstore

    # async def get_crawai_llm(self, name: str = "chat"):
    #     # llm_item = await self.get_llm_config(name)
    #     # def my_custom_logging_fn(model_call_dict):
    #     #     print(f"model call details=======================: {model_call_dict}")

    #     return LLM(
    #         model="openai/llama3.1-70b",
    #         # temperature=llm_item.temperature or None,
    #         base_url="https://llama3-1-70b.lepton.run/api/v1/",
    #         api_key="iByWYsIUIBe6qRYBswhLVPRyiVKkYb8r",
    #         num_retries=5,
    #         # logger_fn=my_custom_logging_fn,
    # )

    async def get_llm_openai(self, llm_config_name: str):
        # llm_item = await self.get_llm_config(llm_config_name)

        # base_url = llm_item.base_url
        # model = llm_item.model

        # all_llm_providers_prefix = ["together_ai/", "groq/"]
        # 		Model:      "openai/llama3.1-70b",
        # ApiKey:     mtutils.Ptr("CzEDAeske7RipomNe3KLLtqvu820Ewfp"),
        # BaseUrl:    mtutils.Ptr("https://llama3-1-70b.lepton.run/api/v1/"),

        # for prefix in all_llm_providers_prefix:
        #     if model.startswith(prefix):
        #         model = model[len(prefix) :]
        #         break
        return ChatOpenAI(
            base_url="https://llama3-1-70b.lepton.run/api/v1/",
            api_key="CzEDAeske7RipomNe3KLLtqvu820Ewfp",  # type: ignore
            model="openai/llama3.1-70b",
            temperature=0,
            # max_tokens=None,
            # 使用自定义 httpx 客户端 方便日志查看
            http_client=httpx.Client(transport=LoggingTransport()),  # type: ignore
            http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
        )

    async def ainvoke_model(
        self,
        tpl: ChatPromptTemplate,
        inputs: dict | BaseModel | None,
        *,
        tools: list[StructuredTool | dict]|None = None,
        structured_output: BaseModel|None = None,
        llm_config_name: str = "chat",
        max_retries: int = 5,
        sleep_time: int = 3,
    ):
        llm_inst = await self.get_llm_openai(llm_config_name)

        if tools is not None and len(tools) > 0:
            formatted_tools = [
                convert_to_openai_function(tool, strict=True) for tool in tools
            ]
            all_tool_names = [t["name"] for t in formatted_tools]
            all_tool_names_str = ", ".join(all_tool_names)
            if tools and llm_inst.llm_type == "llama3.1":
                # for openai_fun in openai_functions:
                #     tool_call_prompts.append(f"""\nUse the function '{openai_fun["name"]}' to '{openai_fun["description"]}':\n{json.dumps(openai_fun)}\n""")
                # llama3.1 模型工具调用专用提示词，确保工具调用的准确性和一致性
                toolPrompt = f"""
    all tools: {all_tool_names_str}
    [IMPORTANT] When calling a function, adhere strictly to the following guidelines:
    1. Use the exact OpenAI ChatGPT function calling format.
    2. Function calls must be in this format: {{\"name\": \"function_name\", \"arguments\": {{\"arg1\": \"value1\", \"arg2\": \"value2\"}}}}
    3. Only call one function at a time.
    4. Do not include any additional text with the function call.
    5. If no function call is needed, respond normally without mentioning functions.
    6. Only use functions from the provided list of tools.
    7. Function names must consist solely of lowercase letters (a-z), numbers (0-9), and underscores (_).
    8. Ensure all required parameters for the function are included.
    9. Double-check that the function name and all parameter names exactly match those provided in the function description.

    If you're unsure about making a function call, respond to the user's query using your general knowledge instead.
    """
                if "additional_instructions" in tpl.partial_variables:
                    tpl = tpl.partial(additional_instructions=toolPrompt)
                else:
                    tpl.messages.append(
                        ChatPromptTemplate.from_messages([("system", toolPrompt)])
                    )

        if isinstance(inputs, BaseModel):
            inputs = inputs.model_dump()
        messages = await tpl.ainvoke(inputs)
        llm_chain = llm_inst
        if structured_output:
            llm_chain = llm_chain.with_structured_output(
                structured_output, include_raw=True
            )
        if tools:
            llm_chain = llm_chain.bind_tools(tools)
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)

        message_to_post = messages.to_messages()

        for attempt in range(max_retries):
            try:
                invoke_result = await ensure_valid_llm_response_v2(
                    llm_chain, message_to_post
                )
                if isinstance(invoke_result, dict) and "raw" in invoke_result:
                    ai_msg = invoke_result["raw"]
                else:
                    ai_msg = invoke_result
                if tools:
                    ai_msg = utils.fix_tool_calls(ai_msg)

                # 函数名必须是 tools 内，否则必定是不正确的调用，自动重试
                tcs = ai_msg.tool_calls
                if tcs:
                    for tc in tcs:
                        if tc["name"] not in all_tool_names:
                            raise ValueError(
                                f"函数名 {tc['name']} 必须是 tools 内，否则必定是错误"
                            )
                return ai_msg
            except Exception as e:
                if attempt < max_retries - 1:
                    LOG.warning(
                        f"Attempt {attempt + 1} failed. Retrying in 5 seconds..."
                    )
                    await asyncio.sleep(sleep_time)
                else:
                    LOG.error(f"All {max_retries} attempts failed.")
                    raise e

    async def ainvoke_model_with_structured_output(
        self,
        tpl: PromptTemplate,
        inputs: dict | BaseModel | None,
        *,
        tools: list[StructuredTool | dict] = None,
        structured_output: BaseModel,
        llm_config_name: str = "chat",
        max_retries: int = 5,
        sleep_time: int = 3,
    ):
        # llm_item = await self.get_llm_config(llm_config_name)
        llm_inst = await self.get_llm_openai(llm_config_name)

        if tools is not None and len(tools) > 0:
            formatted_tools = [
                convert_to_openai_function(tool, strict=True) for tool in tools
            ]
            all_tool_names = [t["name"] for t in formatted_tools]
            all_tool_names_str = ", ".join(all_tool_names)
            if tools and llm_inst.llm_type == "llama3.1":
                # for openai_fun in openai_functions:
                #     tool_call_prompts.append(f"""\nUse the function '{openai_fun["name"]}' to '{openai_fun["description"]}':\n{json.dumps(openai_fun)}\n""")
                # llama3.1 模型工具调用专用提示词，确保工具调用的准确性和一致性
                toolPrompt = f"""
    all tools: {all_tool_names_str}
    [IMPORTANT] When calling a function, adhere strictly to the following guidelines:
    1. Use the exact OpenAI ChatGPT function calling format.
    2. Function calls must be in this format: {{\"name\": \"function_name\", \"arguments\": {{\"arg1\": \"value1\", \"arg2\": \"value2\"}}}}
    3. Only call one function at a time.
    4. Do not include any additional text with the function call.
    5. If no function call is needed, respond normally without mentioning functions.
    6. Only use functions from the provided list of tools.
    7. Function names must consist solely of lowercase letters (a-z), numbers (0-9), and underscores (_).
    8. Ensure all required parameters for the function are included.
    9. Double-check that the function name and all parameter names exactly match those provided in the function description.

    If you're unsure about making a function call, respond to the user's query using your general knowledge instead.
    """
                if "additional_instructions" in tpl.input_variables:
                    tpl = tpl.partial(additional_instructions=toolPrompt)
                else:
                    tpl.messages.append(
                        ChatPromptTemplate.from_messages([("system", toolPrompt)])
                    )

        if isinstance(inputs, BaseModel):
            inputs = inputs.model_dump()
        messages = await tpl.ainvoke(inputs)
        llm_chain = llm_inst
        if structured_output:
            llm_chain = llm_chain.with_structured_output(
                structured_output, include_raw=True
            )
        if tools:
            llm_chain = llm_chain.bind_tools(tools)
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)

        message_to_post = messages.to_messages()

        for attempt in range(max_retries):
            try:
                invoke_result = await ensure_valid_llm_response_v2(
                    llm_chain, message_to_post
                )
                if isinstance(invoke_result, dict) and "raw" in invoke_result:
                    ai_msg = invoke_result["raw"]
                else:
                    ai_msg = invoke_result
                if tools:
                    ai_msg = utils.fix_tool_calls(ai_msg)

                # 函数名必须是 tools 内，否则必定是不正确的调用，自动重试
                # tcs = ai_msg.tool_calls
                # if tcs:
                #     for tc in tcs:
                #         if tc.name not in all_tool_names:
                #             raise ValueError(
                #                 f"函数名 {tc['name']} 必须是 tools 内，否则必定是错误"
                # )
                return invoke_result
            except Exception as e:
                if attempt < max_retries - 1:
                    LOG.warning(
                        f"Attempt {attempt + 1} failed. Retrying in 5 seconds..."
                    )
                    await asyncio.sleep(sleep_time)
                else:
                    LOG.error(f"All {max_retries} attempts failed.")
                    raise e

    async def stream_messages(self, tpl: ChatPromptTemplate, messages: list[any]):
        messages2 = await tpl.ainvoke({"messages": messages})
        # config = {"configurable": {"thread_id": "abc123"}}
        LOG.info(f"stream_messages: {messages2}")
        llm_inst = await self.get_llm_openai("chat")
        async for chunk in llm_inst.astream(
            messages2,
            # config,
        ):
            if chunk.content:
                yield chunk.content

    def load_json_response(
        self, ai_json_resonse_text: str, model_class: Type[BaseModel]
    ) -> Type[BaseModel]:
        repaired_json = self.repair_json(ai_json_resonse_text)
        try:
            loaded_data = orjson.loads(repaired_json)
            return make_class(**loaded_data)
        except Exception as e:
            LOG.error(f"Error parsing JSON: {str(e)}")
            raise ValueError(
                f"Failed to parse JSON and create {model_class.__name__} instance"
            ) from e

    async def get_db_pool(self):
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        if not settings.MTMAI_DATABASE_URL:
            raise ValueError("MTMAI_DATABASE_URL is not set")
        pool = AsyncConnectionPool(
            conninfo=settings.MTMAI_DATABASE_URL,
            max_size=20,
            kwargs=connection_kwargs,
        )
        await pool.open()
        return pool

    async def checkpointer(self):
        pool = await self.get_db_pool()
        # if not settings.MTMAI_DATABASE_URL:
        #     raise ValueError("MTMAI_DATABASE_URL is not set")
        # db_str = settings.MTMAI_DATABASE_URL
        # checkpointer = AsyncPostgresSaver.from_conn_string(db_str)
        # aa= await AsyncPostgresSaver.from_conn_string(
        #         settings.MTMAI_DATABASE_URL
        #     )

        checkpointer = AsyncPostgresSaver(pool)  # type: ignore
        # if not self.cache_checkpointer:
        #     self.cache_checkpointer = AsyncPostgresSaver.from_conn_string(
        #         settings.MTMAI_DATABASE_URL
        #     )
        return checkpointer

    async def get_graph_by_name(self, name: str):
        if name == "storm":
            from mtmai.agents.storm import StormGraph

            return StormGraph()

        return None

    async def emit(self, evt_name: str, data: dict):
        """发送事件"""
        json1 = json.dumps(data)
        self.hatchet_ctx.put_stream(f"0:{json1}\n")


def init_mtmai_context(hatchetCtx: HatchetContext) -> AgentContext:
    tenant_id = None
    user_id = None
    additional_metadata = hatchetCtx.action.additional_metadata
    if additional_metadata:
        tenant_id = additional_metadata.get("tenantId")
        user_id = additional_metadata.get("userId")
    agent_ctx = AgentContext(tenant_id=tenant_id, user_id=user_id)
    agent_ctx.hatchet_ctx = hatchetCtx
    context_var.set(agent_ctx)
    return agent_ctx


def get_mtmai_context() -> AgentContext:
    try:
        return context_var.get()
    except LookupError:
        raise RuntimeError("mtmai_context  error")


mtmai_context: AgentContext = LazyProxy(get_mtmai_context, enable_cache=False)  # type: ignore
