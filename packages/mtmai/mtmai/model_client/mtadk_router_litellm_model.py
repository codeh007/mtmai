from typing import Any, AsyncGenerator, Dict

from google.adk.models.base_llm import BaseLlm
from google.adk.models.lite_llm import (
    FunctionChunk,
    LiteLLMClient,
    TextChunk,
    _build_request_log,
    _get_completion_inputs,
    _message_to_generate_content_response,
    _model_response_to_chunk,
    _model_response_to_generate_content_response,
)
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from litellm import (
    ChatCompletionAssistantMessage,
    ChatCompletionMessageToolCall,
    Function,
)
from loguru import logger
from pydantic import Field
from typing_extensions import override

from mtmai.model_client.litellm_router import litellm_router


## 主要改变: 使用了 litellm router
class MtAdkLiteRouterLlm(BaseLlm):
    """
    改写 adk 内置的 LiteLlm, 增加自动 重试等功能.
    """

    llm_client: LiteLLMClient = Field(default_factory=LiteLLMClient)
    """The LLM client to use for the model."""

    _additional_args: Dict[str, Any] = None

    def __init__(self, model: str, **kwargs):
        """Initializes the LiteLlm class.

        Args:
            model: The name of the LiteLlm model.
            **kwargs: Additional arguments to pass to the litellm completion api.
        """
        super().__init__(model=model, **kwargs)
        self._additional_args = kwargs
        # preventing generation call with llm_client
        # and overriding messages, tools and stream which are managed internally
        self._additional_args.pop("llm_client", None)
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        # public api called from runner determines to stream or not
        self._additional_args.pop("stream", None)

        ## !!! 关键修改
        self.llm_client = litellm_router

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        """Generates content asynchronously.

        Args:
            llm_request: LlmRequest, the request to send to the LiteLlm model.
            stream: bool = False, whether to do streaming call.

        Yields:
            LlmResponse: The model response.
        """

        logger.info(_build_request_log(llm_request))

        messages, tools = _get_completion_inputs(llm_request)

        completion_args = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
        }
        completion_args.update(self._additional_args)

        if stream:
            text = ""
            function_name = ""
            function_args = ""
            function_id = None
            completion_args["stream"] = True
            for part in self.llm_client.completion(**completion_args):
                for chunk, finish_reason in _model_response_to_chunk(part):
                    if isinstance(chunk, FunctionChunk):
                        if chunk.name:
                            function_name += chunk.name
                        if chunk.args:
                            function_args += chunk.args
                        function_id = chunk.id or function_id
                    elif isinstance(chunk, TextChunk):
                        text += chunk.text
                        yield _message_to_generate_content_response(
                            ChatCompletionAssistantMessage(
                                role="assistant",
                                content=chunk.text,
                            ),
                            is_partial=True,
                        )
                    if finish_reason == "tool_calls" and function_id:
                        yield _message_to_generate_content_response(
                            ChatCompletionAssistantMessage(
                                role="assistant",
                                content="",
                                tool_calls=[
                                    ChatCompletionMessageToolCall(
                                        type="function",
                                        id=function_id,
                                        function=Function(
                                            name=function_name,
                                            arguments=function_args,
                                        ),
                                    )
                                ],
                            )
                        )
                        function_name = ""
                        function_args = ""
                        function_id = None
                    elif finish_reason == "stop" and text:
                        yield _message_to_generate_content_response(
                            ChatCompletionAssistantMessage(
                                role="assistant", content=text
                            )
                        )
                        text = ""

        else:
            response = await self.llm_client.acompletion(**completion_args)

            yield _model_response_to_generate_content_response(response)

    @staticmethod
    @override
    def supported_models() -> list[str]:
        """Provides the list of supported models.

        LiteLlm supports all models supported by litellm. We do not keep track of
        these models here. So we return an empty list.

        Returns:
            A list of supported models.
        """

        return []
