import asyncio
import uuid
from typing import Any, AsyncGenerator, Callable, List, Mapping, Sequence

from autogen_agentchat.base import ChatAgent, TaskResult, Team, TerminationCondition
from autogen_agentchat.messages import (
    AgentEvent,
    ChatMessage,
    ModelClientStreamingChunkEvent,
    TextMessage,
)
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.teams._group_chat._base_group_chat_manager import (
    BaseGroupChatManager,
)
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
    RoundRobinGroupChatManager,
)
from autogen_agentchat.teams._group_chat._selector_group_chat import (
    SelectorGroupChatManager,
)
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    SingleThreadedAgentRuntime,
    TopicId,
)
from autogen_core.models import SystemMessage
from mtmai.agents._types import platform_account_topic_type
from mtmai.agents.ai_agent import AIAgent
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.clients.rest.models.component_model import ComponentModel
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.model_client.utils import get_default_model_client
from typing_extensions import Self


class TenantTeamConfig(RoundRobinGroupChatConfig):
    manager_name: str = "RoundRobinGroupChatManager"


class TenantTeam(BaseGroupChat, Component[TenantTeamConfig]):
    component_provider_override = "mtmai.teams.tenant_team.TenantTeam"
    component_config_schema = TenantTeamConfig

    def __init__(
        self,
        participants: List[ComponentModel] | None = [],
        manager_name: str | None = "RoundRobinGroupChatManager",
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        self.tenant_client = TenantClient()
        self.manager_name = manager_name
        self._runtime = SingleThreadedAgentRuntime(
            # ignore_unhandled_exceptions=False,
        )

        self._termination_condition = termination_condition
        self._max_turns = max_turns

        # Constants for the group chat.
        self._team_id = str(uuid.uuid4())
        self._group_topic_type = "group_topic"
        self._output_topic_type = "output_topic"
        self._group_chat_manager_topic_type = "group_chat_manager"
        # self._participant_topic_types: List[str] = [
        #     participant.name for participant in participants
        # ]
        # self._participant_descriptions: List[str] = [
        #     participant.description for participant in participants
        # ]
        self._collector_agent_type = "collect_output_messages"

        # Constants for the closure agent to collect the output messages.
        self._stop_reason: str | None = None
        self._output_message_queue: asyncio.Queue[AgentEvent | ChatMessage | None] = (
            asyncio.Queue()
        )

        # Create a runtime for the team.
        # TODO: The runtime should be created by a managed context.
        # Background exceptions must not be ignored as it results in non-surfaced exceptions and early team termination.
        self._runtime = SingleThreadedAgentRuntime(
            # ignore_unhandled_exceptions=False,
        )
        self._initialized = False
        self._is_running = False
        self.teams: list[Team] = []

    def _create_group_chat_manager_factory(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[AgentEvent | ChatMessage],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
    ) -> Callable[[], BaseGroupChatManager]:
        def _factory() -> RoundRobinGroupChatManager:
            if self.manager_name == "RoundRobinGroupChatManager":
                return RoundRobinGroupChatManager(
                    name,
                    group_topic_type,
                    output_topic_type,
                    participant_topic_types,
                    participant_names,
                    participant_descriptions,
                    output_message_queue,
                    termination_condition,
                    max_turns,
                )
            elif self.manager_name == "SelectorGroupChatManager":
                return SelectorGroupChatManager(
                    name,
                    group_topic_type,
                    output_topic_type,
                    participant_topic_types,
                    participant_names,
                    participant_descriptions,
                    output_message_queue,
                    termination_condition,
                    max_turns,
                    self._model_client,
                    self._selector_prompt,
                    self._allow_repeated_speaker,
                    self._selector_func,
                    self._max_selector_attempts,
                    self._candidate_func,
                )
            else:
                raise ValueError(f"Invalid manager name: {self.manager_name}")

        return _factory

    async def _init(self, runtime: AgentRuntime):
        self.session_id = get_chat_session_id_ctx()

        # await super()._init(runtime)
        runtime.start()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        session_id = get_chat_session_id_ctx()
        # tenant_id = get_tenant_id()
        model_client = get_default_model_client()
        # Register the sales agent.
        platform_account_type = await AIAgent.register(
            self._runtime,
            type=platform_account_topic_type,  # Using the topic type as the agent type.
            factory=lambda: AIAgent(
                description="A sales agent.",
                system_message=SystemMessage(
                    content="You are a sales agent for ACME Inc."
                    "Always answer in a sentence or less."
                    "Follow the following routine with the user:"
                    "1. Ask them about any problems in their life related to catching roadrunners.\n"
                    "2. Casually mention one of ACME's crazy made-up products can help.\n"
                    " - Don't mention price.\n"
                    "3. Once the user is bought in, drop a ridiculous price.\n"
                    "4. Only after everything, and if the user says yes, "
                    "tell them a crazy caveat and execute their order.\n"
                    ""
                ),
                model_client=model_client,
                tools=[],
                # delegate_tools=[transfer_back_to_triage_tool],
            ),
        )

        await self._runtime.publish_message(
            TextMessage(content="hello", source="user"),
            topic_id=TopicId(platform_account_topic_type, source=session_id),
            # topic_id=platform_account_type,
        )

        # messages: List[ChatMessage] | None = None
        # if task is None:
        #     pass
        # elif isinstance(task, str):
        #     messages = [TextMessage(content=task, source="user")]
        # elif isinstance(task, ChatMessage):
        #     messages = [task]
        # elif isinstance(task, list):
        #     if not task:
        #         raise ValueError("Task list cannot be empty.")
        #     messages = []
        #     for msg in task:
        #         if not isinstance(msg, ChatMessage):
        #             raise ValueError(
        #                 "All messages in task list must be valid ChatMessage types"
        #             )
        #         messages.append(msg)
        # else:
        #     raise ValueError(
        #         "Task must be a string, a ChatMessage, or a list of ChatMessage."
        #     )
        # Check if the messages types are registered with the message factory.
        # if messages is not None:
        #     for msg in messages:
        #         if not self._message_factory.is_registered(msg.__class__):
        #             raise ValueError(
        #                 f"Message type {msg.__class__} is not registered with the message factory. "
        #                 "Please register it with the message factory by adding it to the "
        #                 "custom_message_types list when creating the team."
        #             )

        if self._is_running:
            raise ValueError(
                "The team is already running, it cannot run again until it is stopped."
            )
        self._is_running = True

        # if self._embedded_runtime:
        #     # Start the embedded runtime.
        #     assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #     self._runtime.start()

        if not self._initialized:
            await self._init(self._runtime)

        shutdown_task: asyncio.Task[None] | None = None
        # if self._embedded_runtime:

        #     async def stop_runtime() -> None:
        #         assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #         try:
        #             # This will propagate any exceptions raised.
        #             await self._runtime.stop_when_idle()
        #         finally:
        #             # Stop the consumption of messages and end the stream.
        #             # NOTE: we also need to put a GroupChatTermination event here because when the group chat
        #             # has an exception, the group chat manager may not be able to put a GroupChatTermination event in the queue.
        #             await self._output_message_queue.put(
        #                 GroupChatTermination(
        #                     message=StopMessage(content="Exception occurred.", source=self._group_chat_manager_name)
        #                 )
        #             )

        #     # Create a background task to stop the runtime when the group chat
        #     # is stopped or has an exception.
        #     shutdown_task = asyncio.create_task(stop_runtime())

        try:
            # Run the team by sending the start message to the group chat manager.
            # The group chat manager will start the group chat by relaying the message to the participants
            # and the group chat manager.
            # await self._runtime.send_message(
            #     GroupChatStart(messages=messages),
            #     recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
            #     cancellation_token=cancellation_token,
            # )
            # Collect the output messages in order.
            output_messages: List[AgentEvent | ChatMessage] = []
            stop_reason: str | None = None
            # Yield the messsages until the queue is empty.
            while True:
                message_future = asyncio.ensure_future(self._output_message_queue.get())
                if cancellation_token is not None:
                    cancellation_token.link_future(message_future)
                # Wait for the next message, this will raise an exception if the task is cancelled.
                message = await message_future
                # if isinstance(message, GroupChatTermination):
                #     # If the message is None, it means the group chat has terminated.
                #     # TODO: how do we handle termination when the runtime is not embedded
                #     # and there is an exception in the group chat?
                #     # The group chat manager may not be able to put a GroupChatTermination event in the queue,
                #     # and this loop will never end.
                #     stop_reason = message.message.content
                #     break
                yield message
                if isinstance(message, ModelClientStreamingChunkEvent):
                    # Skip the model client streaming chunk events.
                    continue
                output_messages.append(message)

            # Yield the final result.
            yield TaskResult(messages=output_messages, stop_reason=stop_reason)

        finally:
            try:
                if shutdown_task is not None:
                    # Wait for the shutdown task to finish.
                    # This will propagate any exceptions raised.
                    await shutdown_task
            finally:
                # Clear the output message queue.
                while not self._output_message_queue.empty():
                    self._output_message_queue.get_nowait()

                # Indicate that the team is no longer running.
                self._is_running = False

    # async def run_stream2(
    #     self,
    #     *,
    #     task: str | ChatMessage | Sequence[ChatMessage] | None = None,
    #     cancellation_token: CancellationToken | None = None,
    # ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
    #     if not self._initialized:
    #         await self._init(self._runtime)
    #     # async for event in super().run_stream(
    #     #     task=task, cancellation_token=cancellation_token
    #     # ):
    #     #     if isinstance(event, TaskResult):
    #     #         yield event
    #     #     else:
    #     #         await self.tenant_client.emit(event)
    #     #         yield event

    #     # await self.tenant_client.ag.save_team_state(
    #     #     team=self,
    #     #     componentId=self._team_id,
    #     #     tenant_id=self.tenant_client.tenant_id,
    #     #     chat_id=self.session_id,
    #     # )
    #     await self._runtime.stop_when_idle()

    async def reset(self) -> None:
        # if not self._initialized:
        #     await self._init(self._runtime)

        # if self._is_running:
        #     raise RuntimeError("The group chat is currently running. It must be stopped before it can be reset.")
        # self._is_running = True

        # if self._embedded_runtime:
        #     # Start the runtime.
        #     assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #     self._runtime.start()

        # try:
        #     # Send a reset messages to all participants.
        #     for participant_topic_type in self._participant_topic_types:
        #         await self._runtime.send_message(
        #             GroupChatReset(),
        #             recipient=AgentId(type=participant_topic_type, key=self._team_id),
        #         )
        #     # Send a reset message to the group chat manager.
        #     await self._runtime.send_message(
        #         GroupChatReset(),
        #         recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
        #     )
        # finally:
        #     if self._embedded_runtime:
        #         # Stop the runtime.
        #         assert isinstance(self._runtime, SingleThreadedAgentRuntime)
        #         await self._runtime.stop_when_idle()

        #     # Reset the output message queue.
        #     while not self._output_message_queue.empty():
        #         self._output_message_queue.get_nowait()

        #     # Indicate that the team is no longer running.
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        # state = RoundRobinManagerState(
        #     message_thread=list(self._message_thread),
        #     current_turn=self._current_turn,
        #     next_speaker_index=self._next_speaker_index,
        # )
        # return state.model_dump()
        # state = await super().save_state()
        return {}

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await super().load_state(state)

    def _to_config(self) -> TenantTeamConfig:
        participants = [
            # participant.dump_component() for participant in self._participants
        ]
        termination_condition = (
            # self._termination_condition.dump_component()
            # if self._termination_condition
            # else None
            None
        )
        return TenantTeamConfig(
            participants=participants,
            termination_condition=termination_condition,
            # max_turns=self._max_turns,
        )

    @classmethod
    def _from_config(cls, config: TenantTeamConfig) -> Self:
        session_id = get_chat_session_id_ctx()
        participants = []
        # if hasattr(config, "actual_instance"):
        #     config = config.actual_instance
        # if hasattr(config.participants, "actual_instance"):
        #     config.participants = config.participants.actual_instance
        # config.participants[0].oneof_schema_1_validator.
        for participant in config.participants:
            # if hasattr(participant, "actual_instance") and participant.actual_instance:
            #     participant = participant.actual_instance
            # participant_config = participant.model_dump()
            participants.append(ChatAgent.load_component(participant))
        termination_condition = (
            TerminationCondition.load_component(
                config.termination_condition.model_dump()
            )
            if config.termination_condition
            else None
        )

        needs_user_input_handler = NeedsUserInputHandler(session_id)
        runtime = SingleThreadedAgentRuntime(
            intervention_handlers=[needs_user_input_handler],
            ignore_unhandled_exceptions=False,
        )
        manager_name = config.manager_name
        return cls(
            participants=participants,
            manager_name=manager_name,
            termination_condition=termination_condition,
            max_turns=config.max_turns,
            runtime=runtime,
        )
        #     max_turns=config.max_turns,
        #     runtime=runtime,
        # )
