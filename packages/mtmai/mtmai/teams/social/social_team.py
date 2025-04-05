import asyncio
from typing import Any, AsyncGenerator, Mapping, Sequence

from agents._semantic_router_agent import SemanticRouterAgent
from agents.instagram_agent import InstagramAgent
from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import (
    AgentEvent,
    BaseAgentEvent,
    BaseChatMessage,
    ChatMessage,
)
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
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_event_type import AgentEventType
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.agent_user_input import AgentUserInput
from mtmai.clients.rest.models.instagram_team_config import InstagramTeamConfig
from mtmai.clients.rest.models.social_team_config import SocialTeamConfig
from mtmai.clients.rest.models.state_type import StateType
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.model_client.utils import get_default_model_client
from mtmai.mtlibs.autogen_utils.autogen_utils import (
    MockAgentRegistry,
    MockIntentClassifier,
)
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
        # The queue for collecting the output messages.
        self._output_message_queue: asyncio.Queue[BaseAgentEvent | BaseChatMessage] = (
            asyncio.Queue()
        )

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
                session_id=self.session_id,
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
                model_client=self.model_client,
                user_topic=user_agent_type.type,
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
        task: str | ChatMessage | Sequence[ChatMessage] | AgentRunInput | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        if not self._initialized:
            await self._init()

        team_topic = f"social.{self.session_id}"
        team_topic_id = TopicId(type=team_topic, source="default")
        user_topic_id = TopicId(type=AgentTopicTypes.USER.value, source="default")
        if isinstance(task, AgentRunInput):
            if AgentEventType.AGENTUSERINPUT.value == task.type:
                user_input_msg = AgentUserInput.model_validate(task.model_dump())
                await self._runtime.publish_message(
                    message=user_input_msg,
                    topic_id=user_topic_id,
                    cancellation_token=cancellation_token,
                )

        await self._runtime.stop_when_idle()
        # state = await self.save_state()
        # await self.tenant_client.ag.save_team_state(
        #     componentId=self._team_id,
        #     tenant_id=self.tenant_client.tenant_id,
        #     chat_id=self.session_id,
        #     state=state,
        # )

        # runtime_state = await self._runtime.save_state()
        # logger.info(f"runtime_state: {runtime_state}")
        await self.save_state_db()

    async def reset(self) -> None:
        self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        state = await self._runtime.save_state()
        return state

    async def save_state_db(self):
        state_data = await self.save_state()
        for k, v in state_data.items():
            logger.info(f"key: {k}, value: {v}")
            parts = k.split("/")
            topic = parts[0]
            source = parts[1] if len(parts) > 1 else "default"
            await self.tenant_client.ag_state_api.ag_state_upsert(
                tenant=self.tenant_client.tenant_id,
                ag_state_upsert=AgStateUpsert(
                    tenantId=self.tenant_client.tenant_id,
                    topic=topic,
                    source=source,
                    type=StateType.RUNTIMESTATE.value,
                    chatId=self.session_id,
                    state=v,
                ),
            )

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._runtime.load_state(state)

    def _to_config(self) -> InstagramTeamConfig:
        return SocialTeamConfig(
            max_turns=self._max_turns,
        )

    @classmethod
    def _from_config(cls, config: InstagramTeamConfig) -> Self:
        return cls(
            max_turns=config.max_turns or 25,
        )

    async def pause(self) -> None:
        logger.info("TODO: pause team")

    async def resume(self) -> None:
        logger.info("TODO: resume team")
