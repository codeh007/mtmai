import logging
from typing import Any, Unpack
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    ChatCompletionTokenLogprob,
    CreateResult,
    FinishReasons,
    FunctionExecutionResultMessage,
    LLMMessage,
    ModelCapabilities,  # type: ignore
    ModelFamily,
    ModelInfo,
    RequestUsage,
    SystemMessage,
    TopLogprob,
    UserMessage,
)

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai.config import (
    OpenAIClientConfiguration,
    OpenAIClientConfigurationConfigModel,
)
from json_repair import repair_json

from ..mtmaisdk.context.context import get_gomtm, get_tenant_id
# from ..gomtm_client import get_gomtm_client
# from ..context import get_tenant_id

logger=logging.getLogger(__name__)

class MtmOpenAIChatCompletionClient(OpenAIChatCompletionClient):
    component_type = "model"
    component_config_schema = OpenAIClientConfigurationConfigModel
    component_provider_override = "mtmai.agents.model_client.MtmOpenAIChatCompletionClient"
    def __init__(self, **kwargs: Unpack[OpenAIClientConfiguration]):
        if not kwargs.get("model_info"):
            kwargs["model_info"] = ModelInfo(
                family=ModelFamily.R1,
                vision=False,
                function_calling=True,
                json_output=True,
            )
        super().__init__(**kwargs)
        pass

    def _to_config(self) -> OpenAIClientConfigurationConfigModel:
        # return OpenAIClientConfigurationConfigModel(**copied_config)
        return super()._to_config()


    async def create(self, *args: Any, **kwargs: Any) -> CreateResult:
        """
            如果没有内置的 model config, 则从后端拉取默认的
        """
        try:
            tenant_id = get_tenant_id()
            if not tenant_id:
                raise ValueError("(MtmOpenAIChatCompletionClient)tenant_id is required")
            self.gomtmapi = get_gomtm()

            defaultModel = await self.gomtmapi.model_api.model_get(
                tenant=tenant_id,
                model="default"
            )
            model_dict = defaultModel.config.model_dump()

            model_client = OpenAIChatCompletionClient(
                **model_dict,
            )

            logger.info(f"OpenAI API Request: {args} {kwargs}")
            response = await model_client.create(*args, **kwargs)
            if kwargs.get("json_output", False):
                # 修正json格式
                if isinstance(response.content, str):
                    response.content = repair_json(response.content)

            logger.info(
                "OpenAI API Response",
                request_args=args,
                request_kwargs=kwargs,
                response_content=response.content,
            )
            return response
        except Exception as e:
            logger.exception(
                "Mtm Model Client Error", error=str(e), error_type=type(e).__name__
            )
            raise


