from typing import Any, Unpack

import openai
from autogen_core.models import CreateResult, ModelFamily, ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai.config import (
    OpenAIClientConfiguration,
    OpenAIClientConfigurationConfigModel,
)
from json_repair import repair_json


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
        super().__init__(**kwargs)

    def _to_config(self) -> OpenAIClientConfigurationConfigModel:
        return super()._to_config()

    async def create(self, *args: Any, **kwargs: Any) -> CreateResult:
        try:
            response = await super().create(*args, **kwargs)
            if kwargs.get("json_output", False):
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
            # logger.exception(
            #     "Mtm Model Client Error", error=str(e), error_type=type(e).__name__
            # )
            raise e
