from google.adk.models.lite_llm import LiteLlm

from mtmai.model_client.litellm_router import get_litellm_router


class MtAdkRouterLiteLlm(LiteLlm):
  def __init__(self, model: str, **kwargs):
    super().__init__(model=model, **kwargs)
    self.llm_client = get_litellm_router()


# 备份代码
# class MtAdkRouterLiteLlm(BaseLlm):
#   """Wrapper around litellm.

#   This wrapper can be used with any of the models supported by litellm. The
#   environment variable(s) needed for authenticating with the model endpoint must
#   be set prior to instantiating this class.

#   Example usage:
#   ```
#   os.environ["VERTEXAI_PROJECT"] = "your-gcp-project-id"
#   os.environ["VERTEXAI_LOCATION"] = "your-gcp-location"

#   agent = Agent(
#       model=MtAdkLiteLlm(model="vertex_ai/claude-3-7-sonnet@20250219"),
#       ...
#   )
#   ```

#   Attributes:
#     model: The name of the LiteLlm model.
#     llm_client: The LLM client to use for the model.
#   """

#   llm_client: LiteLLMClient = Field(default_factory=LiteLLMClient)
#   """The LLM client to use for the model."""

#   _additional_args: Dict[str, Any] = None

#   def __init__(self, model: str, **kwargs):
#     """Initializes the LiteLlm class.

#     Args:
#       model: The name of the LiteLlm model.
#       **kwargs: Additional arguments to pass to the litellm completion api.
#     """
#     super().__init__(model=model, **kwargs)
#     self._additional_args = kwargs
#     # preventing generation call with llm_client
#     # and overriding messages, tools and stream which are managed internally
#     self._additional_args.pop("llm_client", None)
#     self._additional_args.pop("messages", None)
#     self._additional_args.pop("tools", None)
#     # public api called from runner determines to stream or not
#     self._additional_args.pop("stream", None)

#     ## !!! 关键修改
#     self.llm_client = get_litellm_router()

#   async def generate_content_async(
#     self, llm_request: LlmRequest, stream: bool = False
#   ) -> AsyncGenerator[LlmResponse, None]:
#     """Generates content asynchronously.

#     Args:
#       llm_request: LlmRequest, the request to send to the LiteLlm model.
#       stream: bool = False, whether to do streaming call.

#     Yields:
#       LlmResponse: The model response.
#     """

#     self._maybe_append_user_content(llm_request)
#     logger.debug(_build_request_log(llm_request))

#     messages, tools = _get_completion_inputs(llm_request)

#     completion_args = {
#       "model": self.model,
#       "messages": messages,
#       "tools": tools,
#     }
#     completion_args.update(self._additional_args)

#     if stream:
#       text = ""
#       function_name = ""
#       function_args = ""
#       function_id = None
#       completion_args["stream"] = True
#       aggregated_llm_response = None
#       aggregated_llm_response_with_tool_call = None
#       usage_metadata = None

#       for part in self.llm_client.completion(**completion_args):
#         for chunk, finish_reason in _model_response_to_chunk(part):
#           if isinstance(chunk, FunctionChunk):
#             if chunk.name:
#               function_name += chunk.name
#             if chunk.args:
#               function_args += chunk.args
#             function_id = chunk.id or function_id
#           elif isinstance(chunk, TextChunk):
#             text += chunk.text
#             yield _message_to_generate_content_response(
#               ChatCompletionAssistantMessage(
#                 role="assistant",
#                 content=chunk.text,
#               ),
#               is_partial=True,
#             )
#           elif isinstance(chunk, UsageMetadataChunk):
#             usage_metadata = types.GenerateContentResponseUsageMetadata(
#               prompt_token_count=chunk.prompt_tokens,
#               candidates_token_count=chunk.completion_tokens,
#               total_token_count=chunk.total_tokens,
#             )

#           if finish_reason == "tool_calls" and function_id:
#             aggregated_llm_response_with_tool_call = _message_to_generate_content_response(
#               ChatCompletionAssistantMessage(
#                 role="assistant",
#                 content="",
#                 tool_calls=[
#                   ChatCompletionMessageToolCall(
#                     type="function",
#                     id=function_id,
#                     function=Function(
#                       name=function_name,
#                       arguments=function_args,
#                     ),
#                   )
#                 ],
#               )
#             )
#             function_name = ""
#             function_args = ""
#             function_id = None
#           elif finish_reason == "stop" and text:
#             aggregated_llm_response = _message_to_generate_content_response(
#               ChatCompletionAssistantMessage(role="assistant", content=text)
#             )
#             text = ""

#       # waiting until streaming ends to yield the llm_response as litellm tends
#       # to send chunk that contains usage_metadata after the chunk with
#       # finish_reason set to tool_calls or stop.
#       if aggregated_llm_response:
#         if usage_metadata:
#           aggregated_llm_response.usage_metadata = usage_metadata
#           usage_metadata = None
#         yield aggregated_llm_response

#       if aggregated_llm_response_with_tool_call:
#         if usage_metadata:
#           aggregated_llm_response_with_tool_call.usage_metadata = usage_metadata
#         yield aggregated_llm_response_with_tool_call

#     else:
#       response = await self.llm_client.acompletion(**completion_args)
#       yield _model_response_to_generate_content_response(response)

#   @staticmethod
#   @override
#   def supported_models() -> list[str]:
#     """Provides the list of supported models.

#     LiteLlm supports all models supported by litellm. We do not keep track of
#     these models here. So we return an empty list.

#     Returns:
#       A list of supported models.
#     """

#     return []
