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
from loguru import logger
from openai import OpenAI

from mtmai.core.config import settings

# 常见错误代码:
# 402: Payment Required


class MtmOpenAIChatCompletionClient(OpenAIChatCompletionClient):
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

    # def _to_config(self) -> OpenAIClientConfigurationConfigModel:
    #     return super()._to_config()

    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> CreateResult:
        custom_model_client = OpenAIChatCompletionClient(
            model=self.config.get("model", "deepseek-ai/deepseek-r1"),
            base_url=self.config.get("base_url", "https://integrate.api.nvidia.com/v1"),
            api_key=self.config.get("api_key", settings.OPENAI_API_KEY),
            max_tokens=self.config.get("max_tokens", 64 * 1024),
            temperature=self.config.get("temperature", 0.6),
            top_p=self.config.get("top_p", 0.7),
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
            raise e
        except Exception as e:
            logger.exception(
                "Mtm Model Client Error", error=str(e), error_type=type(e).__name__
            )
            # logger.info(
            #     "model_client_error",
            #     messages=messages,
            #     tools=tools,
            #     # content=response.,
            # )
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
