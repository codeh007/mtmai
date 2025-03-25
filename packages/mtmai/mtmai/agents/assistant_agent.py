# class InstagramAgent(AssistantAgent, Component[InstagramAgentConfig]):
#     component_config_schema = InstagramAgentConfig
#     component_provider_override = "mtmai.agents.assistant_agent.AssistantAgent"

#     def __init__(
#         self,
#         name: str,
#         model_client: ChatCompletionClient,
#         *,
#         tools: List[
#             BaseTool[Any, Any] | Callable[..., Any] | Callable[..., Awaitable[Any]]
#         ]
#         | None = None,
#         handoffs: List[HandoffBase | str] | None = None,
#         model_context: ChatCompletionContext | None = None,
#         description: str = "An agent that provides assistance with ability to use tools.",
#         system_message: (
#             str | None
#         ) = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed.",
#         model_client_stream: bool = False,
#         reflect_on_tool_use: bool = False,
#         tool_call_summary_format: str = "{result}",
#         memory: Sequence[Memory] | None = None,
#     ) -> None:
#         super().__init__(
#             name=name,
#             model_client=model_client,
#             tools=tools,
#             handoffs=handoffs,
#             model_context=model_context,
#             description=description,
#             system_message=system_message,
#             model_client_stream=model_client_stream,
#             reflect_on_tool_use=reflect_on_tool_use,
#             tool_call_summary_format=tool_call_summary_format,
#             memory=memory,
#         )

#     # @message_handler
#     # async def handle_user_task(self, message: UserTask, ctx: MessageContext) -> None:
#     #     # human_input = input("Human agent input: ")
#     #     human_input = await self.get_user_input("Human agent input: ")
#     #     logger.info("TODO: need human input")
#     #     logger.info(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
#     #     message.context.append(
#     #         AssistantMessage(content=human_input, source=self.id.type)
#     #     )
#     #     await self.publish_message(
#     #         AgentResponse(
#     #             context=message.context, reply_to_topic_type=self._agent_topic_type
#     #         ),
#     #         topic_id=TopicId(self._user_topic_type, source=self.id.key),
#     # )

#     async def on_messages(
#         self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
#     ) -> Response:
#         async for message in self.on_messages_stream(messages, cancellation_token):
#             if isinstance(message, Response):
#                 return message
#         raise AssertionError("The stream should have returned the final result.")

#     @classmethod
#     def _from_config(cls, config: AgentConfig | InstagramAgentConfig) -> Self:
#         """Create an assistant agent from a declarative config."""

#         _config = config
#         if isinstance(config, AgentConfig):
#             # _config=config.
#             return cls(
#                 name=config.name,
#                 model_client=ChatCompletionClient.load_component(config.model_client),
#                 tools=[BaseTool.load_component(tool) for tool in config.tools]
#                 if config.tools
#                 else None,
#                 handoffs=config.handoffs,
#                 model_context=None,
#                 memory=[Memory.load_component(memory) for memory in config.memory]
#                 if config.memory
#                 else None,
#                 description=config.description,
#             )
#         else:
#             return cls(
#                 name=config.name,
#                 model_client=ChatCompletionClient.load_component(
#                     config.model_client.model_dump()
#                 ),
#                 tools=[BaseTool.load_component(tool) for tool in config.tools]
#                 if config.tools
#                 else None,
#                 handoffs=config.handoffs,
#                 model_context=None,
#                 memory=[Memory.load_component(memory) for memory in config.memory]
#                 if config.memory
#                 else None,
#                 description=config.description,
#                 system_message=config.system_message,
#                 model_client_stream=config.model_client_stream,
#                 reflect_on_tool_use=config.reflect_on_tool_use,
#                 tool_call_summary_format=config.tool_call_summary_format,
#             )
