from typing import Any, AsyncGenerator, Mapping, Sequence

from agents.user_agent import UserAgent
from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    Component,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
    try_get_known_serializers_for_type,
)
from loguru import logger
from mtmai.agents._semantic_router_agent import SemanticRouterAgent
from mtmai.agents._types import AgentRegistryBase, agent_message_types
from mtmai.agents.instagram_agent import InstagramAgent
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.agent_user_input import AgentUserInput
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.model_client.utils import get_default_model_client
from mtmai.teams.sys_team import MockIntentClassifier
from pydantic import BaseModel
from typing_extensions import Self


class TestTeamConfig(BaseModel):
    max_turns: int | None = None


class MockAgentRegistry(AgentRegistryBase):
    def __init__(self):
        self.agents = {
            "finance_intent": "finance",
            "hr_intent": "hr",
            # "general": triage_agent_topic_type,
        }

    async def get_agent(self, intent: str) -> str:
        return self.agents[intent]


class TestTeam(Team, Component[TestTeamConfig]):
    component_provider_override = "mtmai.teams.test_team.TestTeam"
    component_config_schema = TestTeamConfig

    def __init__(
        self,
    ) -> None:
        self._initialized = False
        self._is_running = False

    async def _init(self, runtime: AgentRuntime):
        self.session_id = get_chat_session_id_ctx()
        self._initialized = True
        self.tenant_client = TenantClient()
        for t in agent_message_types:
            runtime.add_message_serializer(try_get_known_serializers_for_type(t))

        # Create the Semantic Router
        agent_registry = MockAgentRegistry()
        intent_classifier = MockIntentClassifier()
        router_agent_type = await SemanticRouterAgent.register(
            runtime=runtime,
            type=AgentTopicTypes.ROUTER.value,
            factory=lambda: SemanticRouterAgent(
                name="router",
                agent_registry=agent_registry,
                intent_classifier=intent_classifier,
            ),
        )

        self.model_client = get_default_model_client()

        await runtime.add_subscription(
            TypeSubscription(
                topic_type=AgentTopicTypes.ROUTER.value,
                agent_type=router_agent_type.type,
            )
        )

        user_agent_type = await UserAgent.register(
            runtime=runtime,
            type=AgentTopicTypes.USER.value,
            factory=lambda: UserAgent(
                description="A user agent.",
            ),
        )
        await runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=AgentTopicTypes.USER.value, agent_type=user_agent_type.type
            )
        )
        instagram_agent_type = await InstagramAgent.register(
            runtime=runtime,
            type=AgentTopicTypes.INSTAGRAM.value,
            factory=lambda: InstagramAgent(),
        )
        await runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=instagram_agent_type, agent_type=instagram_agent_type.type
            )
        )

        runtime.start()

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | AgentUserInput | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if cancellation_token and cancellation_token.is_cancelled():
            logger.info("cancellation_token is cancelled")
            return

        session_id = get_chat_session_id_ctx()
        needs_user_input_handler = NeedsUserInputHandler(session_id)
        self._runtime = SingleThreadedAgentRuntime(
            intervention_handlers=[needs_user_input_handler],
            ignore_unhandled_exceptions=False,
        )
        if not self._initialized:
            await self._init(self._runtime)

        await self._runtime.load_state(
            {
                "User/b59add05-9f88-4379-a50c-e75f6bffdb90": {
                    "model_context": "model_context",
                },
            }
        )
        if isinstance(task, str):
            await self._runtime.publish_message(
                message=AgentUserInput(content=task),
                topic_id=TopicId(
                    type=AgentTopicTypes.INSTAGRAM.value, source=self.session_id
                ),
            )
        else:
            await self._runtime.publish_message(
                message=task,
                topic_id=TopicId(
                    type=AgentTopicTypes.USER.value, source=self.session_id
                ),
            )

            # agent_id = AgentId(instagram_agent_topic_type, "default")
            # await self._runtime.send_message(task, agent_id)

        await self._runtime.stop_when_idle()
        state = await self._runtime.save_state()

        return state

    async def reset(self) -> None:
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        state = await self._runtime.save_state()
        return state

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._runtime.load_state(state)

    def _to_config(self) -> TestTeamConfig:
        participants = [
            participant.dump_component() for participant in self._participants
        ]
        termination_condition = (
            self._termination_condition.dump_component()
            if self._termination_condition
            else None
        )
        return TestTeamConfig(
            participants=participants,
            model_client=self._model_client.dump_component(),
            termination_condition=termination_condition,
            max_turns=self._max_turns,
            max_stalls=self._max_stalls,
            final_answer_prompt=self._final_answer_prompt,
        )

    @classmethod
    def _from_config(cls, config: TestTeamConfig) -> Self:
        return cls()

    @classmethod
    def from_new(cls) -> Self:
        return cls()

    # async def reset(self) -> None:
    #     """Reset the team and all its participants to its initial state."""
    #     ...

    async def pause(self) -> None:
        """Pause the team and all its participants. This is useful for
        pausing the :meth:`autogen_agentchat.base.TaskRunner.run` or
        :meth:`autogen_agentchat.base.TaskRunner.run_stream` methods from
        concurrently, while keeping them alive."""
        ...

    async def resume(self) -> None:
        """Resume the team and all its participants from a pause after
        :meth:`pause` was called."""
        ...
