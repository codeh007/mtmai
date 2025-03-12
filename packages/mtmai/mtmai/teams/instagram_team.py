from typing import Any, AsyncGenerator, Mapping, Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff, TaskResult, TerminationCondition
from autogen_agentchat.conditions import (
    HandoffTermination,
    MaxMessageTermination,
    TextMentionTermination,
)
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    SingleThreadedAgentRuntime,
)
from autogen_ext.tools.mcp import mcp_server_tools
from loguru import logger
from model_client.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents._agents import MtAssistantAgent
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.agents.termination import MyFunctionCallTermination
from mtmai.clients.rest.models.instagram_team_config import InstagramTeamConfig
from mtmai.mtlibs.mcp import print_mcp_tools


def wait_user_approval(prompt: str) -> str:
    """暂停对话,等用户通过UI批准后,继续对话"""
    logger.info(f"(wait_user_approval): {prompt}")
    return f"等待用户确认: {prompt}"


class InstagramTeam(SelectorGroupChat, Component[InstagramTeamConfig]):
    component_type = "mtmai.teams.instagram_team.InstagramTeam"
    component_label = "InstagramTeam"
    component_description = "InstagramTeam"

    def __init__(
        self,
        # participants: List[ComponentModel] = [],
        model_client: MtmOpenAIChatCompletionClient | None = None,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        self._runtime = runtime
        self._is_embedded_runtime = False
        self.needs_user_input_handler = NeedsUserInputHandler()
        if self._runtime is None:
            self._runtime = SingleThreadedAgentRuntime(
                intervention_handlers=[
                    self.needs_user_input_handler,
                ]
            )
            self._is_embedded_runtime = True
        self._initialized = False
        self._is_running = False
        self.termination_condition = termination_condition
        self.max_turns = max_turns
        self._model_client = model_client

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
        from mtmai.context.context_client import TenantClient

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
        tenant_client = TenantClient()
        self._chat_model_client = await tenant_client.ag.get_tenant_model_client(
            tid=tenant_client.tenant_id, model_name="chat"
        )
        tools = await mcp_server_tools(await tenant_client.get_mcp_endpoint())

        print_mcp_tools(tools)
        planning_agent = MtAssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=self._chat_model_client,
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

        # Create a lazy assistant agent that always hands off to the user.
        writer = AssistantAgent(
            "WriterAgent",
            description="专业的博客文章写手",
            model_client=self._chat_model_client,
            handoffs=[Handoff(target="user", message="Transfer to user.")],
            system_message="你是专业的博客文章写手,擅长编写符合SEO规则的文章,熟悉不同社交媒体的规则"
            "If you cannot complete the task, transfer to user. Otherwise, when finished, respond with 'TERMINATE'.",
        )

        fetch_agent = AssistantAgent(
            name="content_fetcher",
            model_client=self._chat_model_client,
            tools=tools,  # The MCP fetch tool will be included here
            system_message="你是一个网页内容获取助手。使用 fetchWebContent 工具获取网页内容。。当找不到合适工具时,回复: I need xxx tool, TERMINATE",
        )
        rewriter_agent = AssistantAgent(
            name="content_rewriter",
            model_client=self._model_client,
            system_message="""你是一个内容改写专家。将提供给你的网页内容改写为科技资讯风格的文章。
        科技资讯风格特点：
        1. 标题简洁醒目
        2. 开头直接点明主题
        3. 内容客观准确但生动有趣
        4. 使用专业术语但解释清晰
        5. 段落简短，重点突出

        当你完成改写后，回复TERMINATE。""",
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
            # | my_function_call_termination
            # | handoff_termination
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
        # self.inner_team = SelectorGroupChat(
        #     participants=[planning_agent, writer],
        #     termination_condition=termination,
        #     model_client=self.model_client,
        #     allow_repeated_speaker=True,
        #     max_turns=self.max_turns or 25,
        #     runtime=self._runtime,
        # )
        self.inner_team = RoundRobinGroupChat(
            participants=[fetch_agent, rewriter_agent],
            termination_condition=termination,
            max_turns=self.max_turns or 25,
            runtime=self._runtime,
        )
        self._initialized = True
        if self._is_embedded_runtime:
            self._runtime.start()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if not self._initialized:
            await self._init(self._runtime)
        # Use async for to yield events from inner_team's run_stream
        async for event in self.inner_team.run_stream(
            task=task, cancellation_token=cancellation_token
        ):
            yield event
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

    async def save_state(self) -> Mapping[str, Any]:
        if not self._initialized:
            await self._init(self._runtime)

        return await self.inner_team.save_state()

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
