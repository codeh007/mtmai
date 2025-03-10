from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult, TerminationCondition
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    ComponentModel,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
)
from loguru import logger
from mtmai.agents._agents import (
    MtAssistantAgent,
    scheduling_assistant_topic_type,
    user_topic_type,
)
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.termination import MyFunctionCallTermination
from pydantic import BaseModel

from ..agents._types import AssistantTextMessage, UserTextMessage
from ..agents.intervention_handlers import NeedsUserInputHandler, TerminationHandler
from ..agents.slow_user_proxy_agent import SchedulingAssistantAgent, SlowUserProxyAgent
from ..context.ctx import get_chat_session_id_ctx


def wait_user_approval(prompt: str) -> str:
    """暂停对话,等用户通过UI批准后,继续对话"""
    logger.info(f"(wait_user_approval): {prompt}")
    return f"等待用户确认: {prompt}"


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
        # if runtime is None:
        # runtime = SingleThreadedAgentRuntime()

        # termination_handler = TerminationHandler()
        # needs_user_input_handler = NeedsUserInputHandler()
        # runtime = SingleThreadedAgentRuntime(
        #     intervention_handlers=[needs_user_input_handler, termination_handler]
        # )
        self._runtime = runtime
        self._initialized = False

        test_assisant = MtAssistantAgent(
            name="test_assisant",
            description="test_assisant",
            model_client=model_client,
        )

        planning_agent = MtAssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=model_client,
            # tools=[wait_user_approval],
            system_message="""
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            Your team members are:
                WebSearchAgent: Searches for information
                DataAnalystAgent: Performs calculations

            You only plan and delegate tasks - you do not execute them yourself.

            When assigning tasks, use this format:
            1. <agent> : <task>
            After all tasks are complete, summarize the findings and end with "TERMINATE".
            """,
        )
        participants.append(test_assisant)
        participants.append(planning_agent)

        instagram_assistant = MtAssistantAgent(
            name="UserProxyAssistant",
            description="用户确认助理,当任务计划编排完成后, 用户需要确认后, 你再执行任务",
            model_client=model_client,
            tools=[wait_user_approval],
            system_message="""
            你是一个instagram助手, 当用户需要你执行任务时, 你应该主动调用"wait_user_approval"工具, 等待用户通过UI批准后, 继续执行任务
            """,
        )
        participants.append(instagram_assistant)

        # 可选
        def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
            if messages[-1].source != planning_agent.name:
                return planning_agent.name

            if len(messages) > 4:
                return instagram_assistant.name

            return None

        max_messages_termination = MaxMessageTermination(max_messages=25)
        my_function_call_termination = MyFunctionCallTermination(
            function_name="TERMINATE"
        )
        termination = max_messages_termination & my_function_call_termination
        selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from:
{participants}"
to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.

当任务计划编排完成后, 应该由 UserProxyAssistant 请求用户的确认.

"""

        super().__init__(
            participants=participants,
            termination_condition=termination,
            model_client=model_client,
            allow_repeated_speaker=True,
            max_turns=10,
            runtime=runtime,
            selector_prompt=selector_prompt,
            selector_func=selector_func,
        )

    async def _init(self):
        self.termination_handler = TerminationHandler()
        self.needs_user_input_handler = NeedsUserInputHandler()
        if self._runtime is None:
            self._runtime = SingleThreadedAgentRuntime(
                intervention_handlers=[
                    self.needs_user_input_handler,
                    self.termination_handler,
                ]
            )
        self.user_agent_type = await SlowUserProxyAgent.register(
            self._runtime, "User", lambda: SlowUserProxyAgent("User", "I am a user")
        )
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=user_topic_type, agent_type=self.user_agent_type.type
            )
        )

        self.initial_schedule_assistant_message = AssistantTextMessage(
            content="Hi! How can I help you? I can help schedule meetings",
            source="User",
        )
        self.scheduling_assistant_agent_type = await SchedulingAssistantAgent.register(
            self._runtime,
            scheduling_assistant_topic_type,
            lambda: SchedulingAssistantAgent(
                "SchedulingAssistant",
                description="AI that helps you schedule meetings",
                model_client=self._model_client,
                initial_message=self.initial_schedule_assistant_message,
            ),
        )
        await self._runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=scheduling_assistant_topic_type,
                agent_type=self.scheduling_assistant_agent_type.type,
            )
        )

        self._initialized = True

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if not self._initialized:
            await self._init()

        session_id = get_chat_session_id_ctx()

        initial_schedule_assistant_message = AssistantTextMessage(
            content="Hi! How can I help you? I can help schedule meetings",
            source="User",
        )
        runtime_initiation_message: UserTextMessage | AssistantTextMessage
        latest_user_input = None
        if latest_user_input is not None:
            runtime_initiation_message = UserTextMessage(
                content=latest_user_input, source="User"
            )
        else:
            runtime_initiation_message = initial_schedule_assistant_message
        # state = state_persister.load_content()

        await self._runtime.publish_message(
            message=runtime_initiation_message,
            # topic_id=TopicId(type=scheduling_assistant_topic_type, source=session_id),
            topic_id=TopicId(type=self.user_agent_type.type, source=session_id),
        )
        self._runtime.start()
        await self._runtime.stop_when(
            lambda: self.termination_handler.is_terminated
            or self.needs_user_input_handler.needs_user_input
        )

        user_input_needed = None
        if self.needs_user_input_handler.user_input_content is not None:
            user_input_needed = self.needs_user_input_handler.user_input_content
        elif self.termination_handler.is_terminated:
            logger.info("Terminated - ", self.termination_handler.termination_msg)

        state_to_persist = await self._runtime.save_state()
        # state_persister.save_content(state_to_persist)
