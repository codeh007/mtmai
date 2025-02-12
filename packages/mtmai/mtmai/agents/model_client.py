from typing import Unpack

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai.config import (
    OpenAIClientConfiguration,
    OpenAIClientConfigurationConfigModel,
)


class MtmOpenAIChatCompletionClient(OpenAIChatCompletionClient):
    """
    官方的 OpenAIChatCompletionClient 有一个问题在于序列化为 component 时,
    会丢失 model_info 信息,因此我们重写了这个类,并添加了 model_info 信息
    """

    def __init__(self, **kwargs: Unpack[OpenAIClientConfiguration]):
        super().__init__(**kwargs)
        self.model_info_to_keep = kwargs["model_info"]

    def _to_config(self) -> OpenAIClientConfigurationConfigModel:
        copied_config = self._raw_config.copy()
        copied_config["model_info"] = self.model_info_to_keep
        return OpenAIClientConfigurationConfigModel(**copied_config)


# class LoggingModelClient:
#     """
#     日志记录模型客户端
#     """

#     def __init__(self, wrapped_client):
#         self.wrapped_client = wrapped_client

#     async def create(self, *args: Any, **kwargs: Any) -> Any:
#         try:
#             response = await self.wrapped_client.create(*args, **kwargs)
#             if kwargs.get("json_output", False):
#                 # 修正json格式
#                 if isinstance(response.content, str):
#                     response.content = repair_json(response.content)

#             logger.info(
#                 "OpenAI API Response",
#                 request_args=args,
#                 request_kwargs=kwargs,
#                 response_content=response.content,
#             )
#             return response
#         except Exception as e:
#             logger.exception(
#                 "OpenAI API Error", error=str(e), error_type=type(e).__name__
#             )
#             raise


def get_oai_Model():
    model_client = MtmOpenAIChatCompletionClient(
        model="deepseek-r1:1.5b",
        base_url="https://llama3-3-70b.lepton.run/api/v1/",
        api_key="YLJU3oah5ZwNv1HzAGOeVwfvDfUWB6yb",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            # "family": ModelFamily.R1,
            "family": "llama3",
        },
    )
    return model_client
