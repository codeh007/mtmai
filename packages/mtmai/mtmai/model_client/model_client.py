import asyncio
from typing import Any, Mapping, Optional, Sequence, Unpack

import openai
from autogen_core import CancellationToken
from autogen_core.models import (
    CreateResult,
    LLMMessage,
    ModelFamily,
    ModelInfo,
    UserMessage,
)
from autogen_core.tools import Tool, ToolSchema
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai.config import (
    OpenAIClientConfiguration,
    OpenAIClientConfigurationConfigModel,
)
from json_repair import repair_json
from langchain_openai import ChatOpenAI
from loguru import logger
from mtmai.core.config import settings
from mtmai.model_client._openai_client import MtOpenAIChatCompletionClient
from openai import OpenAI

# 常见错误代码:
# 402: Payment Required


class MtmOpenAIChatCompletionClient(MtOpenAIChatCompletionClient):
    component_type = "model"
    component_config_schema = OpenAIClientConfigurationConfigModel
    component_provider_override = (
        "mtmai.agents.model_client.MtmOpenAIChatCompletionClient"
    )

    def __init__(self, **kwargs: Unpack[OpenAIClientConfiguration]):
        if not kwargs.get("model_info"):
            kwargs["model_info"] = ModelInfo(
                family=ModelFamily.R1,
                vision=False,
                function_calling=True,
                json_output=True,
            )
        if not kwargs.get("top_p"):
            kwargs["top_p"] = 0.7
        if not kwargs.get("temperature"):
            kwargs["temperature"] = 0.6

        # kwargs["max_tokens"] = 4096
        super().__init__(**kwargs)
        self.config = kwargs

    def convert_to_lc_model(self) -> ChatOpenAI:
        from langchain_nvidia_ai_endpoints import ChatNVIDIA

        # return ChatOpenAI(
        #     model=self.config.get("model", "deepseek-ai/deepseek-r1"),
        #     temperature=self.config.get("temperature", 0.6),
        #     top_p=self.config.get("top_p", 0.7),
        #     max_tokens=self.config.get("max_tokens", 4096),
        #     api_key=self.config.get("api_key", settings.OPENAI_API_KEY),
        #     base_url=self.config.get("base_url", "https://integrate.api.nvidia.com/v1"),
        # )
        api_key = self.config.get("api_key", settings.OPENAI_API_KEY)
        if api_key.startswith("nvapi-"):
            return ChatNVIDIA(
                model="deepseek-ai/deepseek-r1",
                api_key=self.config.get("api_key", settings.OPENAI_API_KEY),
                temperature=self.config.get("temperature", 0.6),
                top_p=self.config.get("top_p", 0.7),
                max_tokens=self.config.get("max_tokens", 8192),
            )
        return ChatOpenAI(
            model=self.config.get("model", "deepseek-ai/deepseek-r1"),
            temperature=self.config.get("temperature", 0.6),
            top_p=self.config.get("top_p", 0.7),
            max_tokens=self.config.get("max_tokens", 4096),
            api_key=api_key,
            base_url=self.config.get("base_url", "https://integrate.api.nvidia.com/v1"),
        )

    async def close(self) -> None:
        logger.info("MtmOpenAIChatCompletionClient close")

    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> CreateResult:
        logger.info("MtmOpenAIChatCompletionClient create")
        custom_model_client = MtOpenAIChatCompletionClient(
            model=self.config.get("model", "deepseek-ai/deepseek-r1"),
            base_url=self.config.get("base_url", "https://integrate.api.nvidia.com/v1"),
            api_key=self.config.get("api_key", settings.OPENAI_API_KEY),
            max_tokens=self.config.get("max_tokens", 64 * 1024),
            temperature=self.config.get("temperature", 0.6),
            top_p=self.config.get("top_p", 0.7),
            max_retries=self.config.get("max_retries", 3),
            model_info=self.config.get(
                "model_info",
                {
                    "vision": False,
                    "function_calling": False,
                    "json_output": False,
                    "family": ModelFamily.R1,
                },
            ),
        )

        response: CreateResult = None
        max_retries = self.config.get("max_retries", 10)
        # extra_create_args["http_client"] = httpx.Client(transport=LoggingTransport())
        # extra_create_args["http_async_client"] = httpx.AsyncClient(
        #     transport=LoggingTransport()
        # )
        # http_client=httpx.Client(transport=LoggingTransport()),
        # http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
        for i in range(max_retries):
            try:
                response = await custom_model_client.create(
                    # response = await super().create(
                    messages=messages,
                    tools=tools,
                    json_output=json_output,
                    extra_create_args=extra_create_args,
                    cancellation_token=cancellation_token,
                )
                if json_output:
                    # 修正json格式
                    if isinstance(response.content, str):
                        response.content = repair_json(response.content)

                # logger.info(
                #     "OpenAI API Response",
                #     request_args=args,
                #     request_kwargs=kwargs,
                #     response_content=response.content,
                # )
                return response
            except openai.RateLimitError as e:
                logger.info("RateLimitError, sleep 10 seconds")
                await asyncio.sleep(10)
                if i == max_retries - 1:
                    raise e
            except Exception as e:
                logger.exception(
                    "Mtm Model Client Error", error=str(e), error_type=type(e).__name__
                )
                raise e


async def test_model_client(apikey: str):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=apikey,
    )

    logger.info("test_model_client start")
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1",
        messages=[{"role": "user", "content": "hello"}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True,
    )

    logger.info("test_model_client response:\n")
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


async def test_model_client2(apikey: str):
    custom_model_client = OpenAIChatCompletionClient(
        model="deepseek-ai/deepseek-r1",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=apikey,
        max_tokens=4096,
        temperature=0.6,
        top_p=0.7,
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": ModelFamily.R1,
        },
    )

    result = await custom_model_client.create(
        [UserMessage(content="hello", source="user")]
    )  # type: ignore
    logger.info(result)
