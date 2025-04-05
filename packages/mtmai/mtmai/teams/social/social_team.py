from typing import Any, AsyncGenerator, Mapping, Sequence

from agents._semantic_router_agent import SemanticRouterAgent
from agents.instagram_agent import InstagramAgent
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
from mtmai.agents._types import agent_message_types
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.agents.user_agent import UserAgent
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.instagram_team_config import InstagramTeamConfig
from mtmai.clients.rest.models.social_team_config import SocialTeamConfig
from mtmai.clients.rest.models.termination_message import TerminationMessage
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.model_client.utils import get_default_model_client
from mtmai.teams.sys_team import MockAgentRegistry, MockIntentClassifier
from typing_extensions import Self


class SocialTeam(Team, Component[SocialTeamConfig]):
    component_provider_override = "mtmai.teams.social.social_team.SocialTeam"
    component_config_schema = SocialTeamConfig

    def __init__(
        self,
        *,
        runtime: AgentRuntime | None = None,
        max_turns: int | None = None,
    ) -> None:
        self._runtime = runtime
        self._initialized = False
        self._max_turns = max_turns

    async def _init(self):
        self.session_id = get_chat_session_id_ctx()
        self.tenant_client = TenantClient()
        self.model_client = get_default_model_client()

        if not self._runtime:
            needs_user_input_handler = NeedsUserInputHandler(self.session_id)
            self._runtime = SingleThreadedAgentRuntime(
                intervention_handlers=[needs_user_input_handler],
                ignore_unhandled_exceptions=False,
            )

        for t in agent_message_types:
            self._runtime.add_message_serializer(try_get_known_serializers_for_type(t))

        # Create the Semantic Router
        agent_registry = MockAgentRegistry()
        intent_classifier = MockIntentClassifier()
        router_agent_type = await SemanticRouterAgent.register(
            runtime=self._runtime,
            type=AgentTopicTypes.ROUTER.value,
            factory=lambda: SemanticRouterAgent(
                name="router",
                agent_registry=agent_registry,
                intent_classifier=intent_classifier,
            ),
        )

        self.model_client = get_default_model_client()

        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=AgentTopicTypes.ROUTER.value,
                agent_type=router_agent_type.type,
            )
        )
        user_agent_type = await UserAgent.register(
            runtime=self._runtime,
            type=AgentTopicTypes.USER.value,
            factory=lambda: UserAgent(
                description="A user agent.",
            ),
        )
        await self._runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=AgentTopicTypes.USER.value, agent_type=user_agent_type.type
            )
        )
        instagram_agent_type = await InstagramAgent.register(
            runtime=self._runtime,
            type=AgentTopicTypes.INSTAGRAM.value,
            factory=lambda: InstagramAgent(
                description="An agent that interacts with instagram v2",
                # name="instagram_agent",
                model_client=self._model_client,
            ),
        )
        await self._runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=AgentTopicTypes.INSTAGRAM.value,
                agent_type=instagram_agent_type.type,
            )
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
            await self._init()

        await self._runtime.publish_message(
            message=TerminationMessage(),
            topic_id=TopicId(type=AgentTopicTypes.INSTAGRAM.value, source="default"),
        )

        await self._runtime.publish_message(
            message=TerminationMessage(),
            topic_id=TopicId(type=AgentTopicTypes.USER.value, source="default"),
        )

        async for event in super().run_stream(
            task=task, cancellation_token=cancellation_token
        ):
            if isinstance(event, TaskResult):
                yield event
            else:
                await self.tenant_client.emit(event)
                yield event

        await self._runtime.stop_when_idle()
        state = await self.save_state()
        await self.tenant_client.ag.save_team_state(
            componentId=self._team_id,
            tenant_id=self.tenant_client.tenant_id,
            chat_id=self.session_id,
            state=state,
        )

        runtime_state = await self._runtime.save_state()
        logger.info(f"runtime_state: {runtime_state}")

    async def reset(self) -> None:
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        state = await self._runtime.save_state()
        return state

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._runtime.load_state(state)

    def _to_config(self) -> InstagramTeamConfig:
        # participants = [
        #     participant.dump_component() for participant in self._participants
        # ]
        # termination_condition = (
        #     self._termination_condition.dump_component()
        #     if self._termination_condition
        #     else None
        # )
        return SocialTeamConfig(
            # participants=participants,
            # model_client=self._model_client.dump_component(),
            # termination_condition=termination_condition,
            max_turns=self._max_turns,
            # max_stalls=self._max_stalls,
            # final_answer_prompt=self._final_answer_prompt,
        )

    @classmethod
    def _from_config(cls, config: InstagramTeamConfig) -> Self:
        return cls(
            max_turns=config.max_turns or 25,
        )

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
