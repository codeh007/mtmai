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
from ..gomtm_client import get_gomtm_client
from ..context import get_tenant_id

logger=logging.getLogger(__name__)

class MtmOpenAIChatCompletionClient(OpenAIChatCompletionClient):
    component_type = "model"
    component_config_schema = OpenAIClientConfigurationConfigModel
    component_provider_override = "mtmai.agents.model_client.MtmOpenAIChatCompletionClient"
    def __init__(self, **kwargs: Unpack[OpenAIClientConfiguration]):
        # _raw_config
        if not kwargs.get("model_info"):
            kwargs["model_info"] = {
                "Family": ModelFamily.R1,
                "Vision": False,
                "FunctionCalling": True,
                "JsonOutput": True,
            }

        #     Model:       "deepseek-ai/deepseek-r1",
		# BaseUrl:     mtutils.Ptr("https://integrate.api.nvidia.com/v1"),
		# ApiKey:      mtutils.Ptr(""),
		# MaxTokens:   mtutils.Ptr(8096),
		# MaxRetries:  mtutils.Ptr(2),
		# Temperature: mtutils.Ptr(float32(0.7)),
		# TopP:        mtutils.Ptr(float32(0.7)),
		# ModelInfo: &gen.ModelInfo{
		# 	Family:          gen.R1,
		# 	Vision:          false,
		# 	FunctionCalling: true,
		# 	JsonOutput:      true,
		# },
        super().__init__(**kwargs)

    def _to_config(self) -> OpenAIClientConfigurationConfigModel:
        # copied_config = self._raw_config.copy()
        # copied_config["model_info"] = self.model_info_to_keep
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
            self.gomtmapi = get_gomtm_client()

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


