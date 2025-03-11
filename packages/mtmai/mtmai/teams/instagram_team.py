from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff, TaskResult, TerminationCondition
from autogen_agentchat.conditions import (
    HandoffTermination,
    MaxMessageTermination,
    TextMentionTermination,
)
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    ComponentModel,
    SingleThreadedAgentRuntime,
)
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from loguru import logger
from mtmai.agents._agents import MtAssistantAgent
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.termination import MyFunctionCallTermination
from pydantic import BaseModel


def wait_user_approval(prompt: str) -> str:
    """暂停对话,等用户通过UI批准后,继续对话"""
    logger.info(f"(wait_user_approval): {prompt}")
    return f"等待用户确认: {prompt}"


# class _HandOffAgent(BaseChatAgent):
#     def __init__(self, name: str, description: str, next_agent: str) -> None:
#         super().__init__(name, description)
#         self._next_agent = next_agent

#     @property
#     def produced_message_types(self) -> Sequence[type[ChatMessage]]:
#         return (HandoffMessage,)

#     async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
#         return Response(
#             chat_message=HandoffMessage(
#                 content=f"Transferred to {self._next_agent}.", target=self._next_agent, source=self.name
#             )
#         )

#     async def on_reset(self, cancellation_token: CancellationToken) -> None:
#         pass


class InstagramTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None
    some_value: str = "some_value"
    result_id: str = None


class InstagramTeam(SelectorGroupChat, Component[InstagramTeamConfig]):
    component_type = "mtmai.teams.instagram_team.InstagramTeam"
    component_label = "InstagramTeam"
    component_description = "InstagramTeam"

    def __init__(
        self,
        participants: List[ComponentModel] = [],
        model_client: MtmOpenAIChatCompletionClient | None = None,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        self._runtime = runtime

        self.needs_user_input_handler = NeedsUserInputHandler()
        if self._runtime is None:
            self._runtime = SingleThreadedAgentRuntime(
                intervention_handlers=[
                    self.needs_user_input_handler,
                ]
            )
        self._initialized = False
        self._is_running = False
        self.termination_condition = termination_condition
        self.max_turns = max_turns

        self._model_client = model_client

        # test_assisant = MtAssistantAgent(
        #     name="test_assisant",
        #     description="test_assisant",
        #     model_client=model_client,
        # )

        # super().__init__(
        #     participants=[planning_agent, writer],
        #     termination_condition=termination,
        #     model_client=model_client,
        #     allow_repeated_speaker=True,
        #     max_turns=max_turns or 25,
        #     runtime=runtime,
        #     selector_prompt=selector_prompt,
        #     # selector_func=selector_func,
        # )

    async def _init(self, runtime: AgentRuntime):
        #     self.session_id = get_chat_session_id_ctx()

        #     self.user_agent_type = await SlowUserProxyAgent.register(
        #         self._runtime, "User", lambda: SlowUserProxyAgent("User", "I am a user")
        #     )
        #     await self._runtime.add_subscription(
        #         TypeSubscription(
        #             topic_type=user_topic_type, agent_type=self.user_agent_type.type
        #         )
        #     )

        #     self.initial_schedule_assistant_message = AssistantTextMessage(
        #         content="Hi! How can I help you? I can help schedule meetings",
        #         source="User",
        #     )
        #     self.scheduling_assistant_agent_type = await SchedulingAssistantAgent.register(
        #         runtime=self._runtime,
        #         type=scheduling_assistant_topic_type,
        #         factory=lambda: SchedulingAssistantAgent(
        #             "SchedulingAssistant",
        #             description="AI that helps you schedule meetings",
        #             model_client=self._model_client,
        #             initial_message=self.initial_schedule_assistant_message,
        #         ),
        #     )
        #     await self._runtime.add_subscription(
        #         subscription=TypeSubscription(
        #             topic_type=scheduling_assistant_topic_type,
        #             agent_type=self.scheduling_assistant_agent_type.type,
        #         )
        #     )

        #     for message_type in agent_message_types:
        #         self._runtime.add_message_serializer(
        #             try_get_known_serializers_for_type(message_type)
        #         )
        #     self._initialized = True
        #     self._runtime.start()

        fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
        tools = await mcp_server_tools(fetch_mcp_server)

        planning_agent = MtAssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=self.model_client,
            # tools=[wait_user_approval],
            handoffs=[Handoff(target="user", message="Transfer to user.")],
            system_message="""
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            Your team members are:
                WebSearchAgent: Searches for information
                DataAnalystAgent: Performs calculations

            You only plan and delegate tasks - you do not execute them yourself.

            When assigning tasks, use this format:
            1. <agent> : <task>

            非常重要, 任务编排计划必须交由用户进行最终确认, 用户确认后, 你再执行任务
            After all tasks are complete, summarize the findings and end with "TERMINATE".
            """,
        )
        # participants.append(test_assisant)
        # participants.append(planning_agent)

        # Create a lazy assistant agent that always hands off to the user.
        writer = AssistantAgent(
            "WriterAgent",
            description="专业的博客文章写手",
            model_client=self.model_client,
            handoffs=[Handoff(target="user", message="Transfer to user.")],
            system_message="你是专业的博客文章写手,擅长编写符合SEO规则的文章,熟悉不同社交媒体的规则"
            "If you cannot complete the task, transfer to user. Otherwise, when finished, respond with 'TERMINATE'.",
        )
        # participants.append(writer)
        # instagram_assistant = MtAssistantAgent(
        #     name="UserProxyAssistant",
        #     description="用户确认助理,当任务计划编排完成后, 用户需要确认后, 你再执行任务",
        #     model_client=model_client,
        #     tools=[wait_user_approval],
        #     system_message="""
        #     你是一个instagram助手, 当用户需要你执行任务时, 你应该主动调用"wait_user_approval"工具, 等待用户通过UI批准后, 继续执行任务
        #     """,
        # )
        # participants.append(instagram_assistant)

        # user_agent = UserAgent(
        #     description="用户代理",
        #     agent_topic_type="User",
        # )
        # participants.append(user_agent)

        def input_func(prompt: str) -> str:
            return "user_input"

        # user_proxy_agent = UserProxyAgent(
        #     name="UserProxyAgent",
        #     description="用户代理",
        #     input_func=input_func,
        # )
        # participants.append(user_proxy_agent)

        # 可选
        def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
            if messages[-1].source != planning_agent.name:
                return planning_agent.name

            if len(messages) > 2:
                return writer.name

            return None

        max_messages_termination = MaxMessageTermination(max_messages=25)
        my_function_call_termination = MyFunctionCallTermination(
            function_name="TERMINATE"
        )
        handoff_termination = HandoffTermination(target="user")
        text_termination = TextMentionTermination("TERMINATE")
        termination = (
            max_messages_termination
            | my_function_call_termination
            | handoff_termination
            | text_termination
        )
        if self.termination_condition:
            termination = termination | self.termination_condition
        selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from:
{participants}"
to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.

"""
        self.inner_team = SelectorGroupChat(
            participants=[planning_agent, writer],
            termination_condition=termination,
            model_client=self.model_client,
            allow_repeated_speaker=True,
            max_turns=self.max_turns or 25,
            runtime=self._runtime,
        )
        self._initialized = True
        self._runtime.start()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if not self._initialized:
            await self._init(self._runtime)
        return self.inner_team.run_stream(
            task=task, cancellation_token=cancellation_token
        )
        # # Create the messages list if the task is a string or a chat message.
        # messages: List[ChatMessage] | None = None
        # if task is None:
        #     pass
        # elif isinstance(task, str):
        #     messages = [TextMessage(content=task, source="user")]
        # elif isinstance(task, BaseChatMessage):
        #     messages = [task]
        # else:
        #     if not task:
        #         raise ValueError("Task list cannot be empty.")
        #     messages = []
        #     for msg in task:
        #         if not isinstance(msg, BaseChatMessage):
        #             raise ValueError(
        #                 "All messages in task list must be valid ChatMessage types"
        #             )
        #         messages.append(msg)
        # if self._is_running:
        #     raise ValueError(
        #         "The team is already running, it cannot run again until it is stopped."
        #     )
        # self._is_running = True
        # initial_schedule_assistant_message = AssistantTextMessage(
        #     content="Hi! How can I help you? I can help schedule meetings",
        #     source="User",
        # )
        # runtime_initiation_message: UserTextMessage | AssistantTextMessage
        # latest_user_input = None
        # if latest_user_input is not None:
        #     runtime_initiation_message = UserTextMessage(
        #         content=latest_user_input, source="User"
        #     )
        # else:
        #     runtime_initiation_message = initial_schedule_assistant_message
        # # state = state_persister.load_content()
        # await self._runtime.publish_message(
        #     message=runtime_initiation_message,
        #     topic_id=TopicId(type=self.user_agent_type.type, source=self.session_id),
        # )

    #     # state_persister.save_content(state_to_persist)

    # async def reset(self) -> None:
    #     # if not self._initialized:
    #     #     await self._init(self._runtime)

    #     # if self._is_running:
    #     #     raise RuntimeError("The group chat is currently running. It must be stopped before it can be reset.")
    #     # self._is_running = True

    #     # if self._embedded_runtime:
    #     #     # Start the runtime.
    #     #     assert isinstance(self._runtime, SingleThreadedAgentRuntime)
    #     #     self._runtime.start()

    #     # try:
    #     #     # Send a reset messages to all participants.
    #     #     for participant_topic_type in self._participant_topic_types:
    #     #         await self._runtime.send_message(
    #     #             GroupChatReset(),
    #     #             recipient=AgentId(type=participant_topic_type, key=self._team_id),
    #     #         )
    #     #     # Send a reset message to the group chat manager.
    #     #     await self._runtime.send_message(
    #     #         GroupChatReset(),
    #     #         recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
    #     #     )
    #     # finally:
    #     #     if self._embedded_runtime:
    #     #         # Stop the runtime.
    #     #         assert isinstance(self._runtime, SingleThreadedAgentRuntime)
    #     #         await self._runtime.stop_when_idle()

    #     #     # Reset the output message queue.
    #     #     while not self._output_message_queue.empty():
    #     #         self._output_message_queue.get_nowait()

    #     #     # Indicate that the team is no longer running.
    #     self._is_running = False

    # async def save_state(self) -> Mapping[str, Any]:
    #     """Save the state of the group chat team.

    #     The state is saved by calling the :meth:`~autogen_core.AgentRuntime.agent_save_state` method
    #     on each participant and the group chat manager with their internal agent ID.
    #     The state is returned as a nested dictionary: a dictionary with key `agent_states`,
    #     which is a dictionary the agent names as keys and the state as values.

    #     .. code-block:: text

    #         {
    #             "agent_states": {
    #                 "agent1": ...,
    #                 "agent2": ...,
    #                 "RoundRobinGroupChatManager": ...
    #             }
    #         }

    #     .. note::

    #         Starting v0.4.9, the state is using the agent name as the key instead of the agent ID,
    #         and the `team_id` field is removed from the state. This is to allow the state to be
    #         portable across different teams and runtimes. States saved with the old format
    #         may not be compatible with the new format in the future.

    #     .. caution::

    #         When calling :func:`~autogen_agentchat.teams.BaseGroupChat.save_state` on a team
    #         while it is running, the state may not be consistent and may result in an unexpected state.
    #         It is recommended to call this method when the team is not running or after it is stopped.

    #     """
    #     if not self._initialized:
    #         await self._init(self._runtime)

    #     # Store state of each agent by their name.
    #     # NOTE: we don't use the agent ID as the key here because we need to be able to decouple
    #     # the state of the agents from their identities in the agent runtime.
    #     agent_states: Dict[str, Mapping[str, Any]] = {}
    #     # Save the state of all participants.
    #     for name, agent_type in zip(
    #         self._participant_names, self._participant_topic_types, strict=True
    #     ):
    #         agent_id = AgentId(type=agent_type, key=self._team_id)
    #         # NOTE: We are using the runtime's save state method rather than the agent instance's
    #         # save_state method because we want to support saving state of remote agents.
    #         agent_states[name] = await self._runtime.agent_save_state(agent_id)
    #     # Save the state of the group chat manager.
    #     agent_id = AgentId(type=self._group_chat_manager_topic_type, key=self._team_id)
    #     agent_states[
    #         self._group_chat_manager_name
    #     ] = await self._runtime.agent_save_state(agent_id)
    #     return TeamState(agent_states=agent_states).model_dump()

    # async def load_state(self, state: Mapping[str, Any]) -> None:
    #     """Load an external state and overwrite the current state of the group chat team.

    #     The state is loaded by calling the :meth:`~autogen_core.AgentRuntime.agent_load_state` method
    #     on each participant and the group chat manager with their internal agent ID.
    #     See :meth:`~autogen_agentchat.teams.BaseGroupChat.save_state` for the expected format of the state.
    #     """
    #     if not self._initialized:
    #         await self._init(self._runtime)

    #     if self._is_running:
    #         raise RuntimeError("The team cannot be loaded while it is running.")
    #     self._is_running = True

    #     try:
    #         team_state = TeamState.model_validate(state)
    #         # Load the state of all participants.
    #         for name, agent_type in zip(
    #             self._participant_names, self._participant_topic_types, strict=True
    #         ):
    #             agent_id = AgentId(type=agent_type, key=self._team_id)
    #             if name not in team_state.agent_states:
    #                 raise ValueError(
    #                     f"Agent state for {name} not found in the saved state."
    #                 )
    #             await self._runtime.agent_load_state(
    #                 agent_id, team_state.agent_states[name]
    #             )
    #         # Load the state of the group chat manager.
    #         agent_id = AgentId(
    #             type=self._group_chat_manager_topic_type, key=self._team_id
    #         )
    #         if self._group_chat_manager_name not in team_state.agent_states:
    #             raise ValueError(
    #                 f"Agent state for {self._group_chat_manager_name} not found in the saved state."
    #             )
    #         await self._runtime.agent_load_state(
    #             agent_id, team_state.agent_states[self._group_chat_manager_name]
    #         )

    #     except ValidationError as e:
    #         raise ValueError(
    #             "Invalid state format. The expected state format has changed since v0.4.9. "
    #             "Please read the release note on GitHub."
    #         ) from e

    #     finally:
    #         # Indicate that the team is no longer running.
    #         self._is_running = False
