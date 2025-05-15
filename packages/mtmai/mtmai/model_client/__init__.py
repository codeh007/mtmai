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
    Router,
)
from loguru import logger
from pydantic import Field
from smolagents import LiteLLMRouterModel
from typing_extensions import override

from mtmai.core.config import settings


def get_model_list():
    model_list = [
        {
            "model_name": "gemini-2.0-flash-exp",
            "litellm_params": {
                "model": "gemini/gemini-2.0-flash-exp",
                "api_key": settings.GOOGLE_AI_STUDIO_API_KEY,
                "max_parallel_requests": 2,
            },
        },
        {
            "model_name": "gemini-2.0-flash-exp2",
            "litellm_params": {
                "api_key": settings.GOOGLE_AI_STUDIO_API_KEY_2,
                "model": "gemini/gemini-2.0-flash-exp",
                "max_parallel_requests": 2,
            },
        },
    ]
    return model_list


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
        self.llm_client = Router(
            model_list=get_model_list(),
            num_retries=5,
            cooldown_time=10,
            retry_after=5,
            fallbacks=[{"gemini-2.0-flash-exp": ["gemini-2.0-flash-exp2"]}],
        )

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


def get_default_litellm_model():
    # return LiteLlm(
    #     # model="openai/nvidia/llama-3.3-nemotron-super-49b-v1",
    #     # model="openai/qwen/qwq-32b",
    #     model="openai/meta/llama-3.3-70b-instruct",
    #     api_key="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",
    #     base_url="https://integrate.api.nvidia.com/v1",
    # )
    # return MtLiteLlm(
    #     # model="openai/nvidia/llama-3.3-nemotron-super-49b-v1",
    #     # model="openai/qwen/qwq-32b",
    #     # model="openai/qwen/qwen-2.5-coder-32b-instruct:free",
    #     # model="openai/qwen/qwq-32b:free",
    #     model="openai/google/gemini-2.5-pro-exp-03-25:free",
    #     api_key=settings.OPENROUTER_API_KEY,
    #     base_url="https://openrouter.ai/api/v1",
    # )
    # return MtLiteLlm(
    #     model="openai/google/gemini-2.5-pro-exp-03-25:free",
    #     api_key=settings.OPENROUTER_API_KEY,
    #     base_url="https://gateway.ai.cloudflare.com/v1/623faf72ee0d2af3e586e7cd9dadb72b/openrouter/openrouter",
    # )

    # return MtLiteLlm(
    #     # model="openai/deepseek-ai/DeepSeek-V3-0324",
    #     model="huggingface/sambanova/meta-llama/Llama-3.3-70B-Instruct",
    #     api_key=settings.HF_TOKEN,
    #     # base_url="https://gateway.ai.cloudflare.com/v1/623faf72ee0d2af3e586e7cd9dadb72b/openrouter/huggingface",
    # )

    # return MtLiteLlm(
    #     # model="openai/nvidia/Llama-3_3-Nemotron-Super-49B-v1",
    #     model="openai/chutesai/Llama-4-Maverick-17B-128E-Instruct-FP8",
    #     api_key="cpk_85dee936b21c481ea7d542176feb9200.e3d47e0e31625c8d950242c2df75d5bf.yiIDLv7Symy5QjdrPuRO7pU6ImMnR9iw",
    #     base_url="https://llm.chutes.ai/v1",
    #     # tool_choice="auto",
    # )

    return MtAdkLiteRouterLlm(
        # model="gemini/gemini-2.5-pro-exp-03-25",
        # model="gemini/gemini-2.0-flash-exp",
        model="gemini-2.0-flash-exp",
        api_key=settings.GOOGLE_AI_STUDIO_API_KEY,
    )


def get_default_smolagents_model():
    model = LiteLLMRouterModel(
        model_id="gemini-2.0-flash-exp2",
        model_list=get_model_list(),
        client_kwargs={
            "routing_strategy": "simple-shuffle",
        },
        num_retries=10,
        cooldown_time=10,
        retry_after=5,
        # fallbacks=[{"gemini-2.0-flash-exp": ["gemini-2.0-flash-exp2"]}],
    )
    return model
