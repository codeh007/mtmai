import asyncio
from textwrap import dedent
from typing import Any, Callable, List, Mapping

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.messages import (
    BaseAgentEvent,
    BaseChatMessage,
    MessageFactory,
    TextMessage,
)
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.teams._group_chat._events import GroupChatTermination
from autogen_core import AgentRuntime, Component, ComponentModel
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.agents.social_team_manager import SocialTeamManager
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.social_team_config import SocialTeamConfig
from mtmai.clients.rest.models.start_new_chat_input import StartNewChatInput
from mtmai.clients.rest.models.state_type import StateType
from mtmai.context.context import Context
from mtmai.model_client.utils import get_default_model_client
from mtmai.worker_app import mtmapp
from pydantic import BaseModel
from typing_extensions import Self


@mtmapp.workflow(
    name=FlowNames.SOCIAL,
    on_events=[FlowNames.SOCIAL],
)
class FlowSocial:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        # input = MtAgEvent.from_dict(hatctx.input)
        input = StartNewChatInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()

        if isinstance(input.config.actual_instance, SocialTeamConfig):
            team = SocialTeam._from_config(
                SocialTeamConfig.from_dict(input.config.actual_instance.model_dump())
            )
        else:
            raise ValueError(
                f"Invalid team config type: {type(input.config.actual_instance)}"
            )

        task = TextMessage(content=input.task, source="user")
        result = await team.run(task=task, cancellation_token=cancellation_token)
        logger.info(f"result: {result}")
        return result


class SocialGroupChatConfig(BaseModel):
    """The declarative configuration SocialTeam."""

    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None


class SocialTeam(BaseGroupChat, Component[SocialGroupChatConfig]):
    component_provider_override = "mtmai.teams.team_social.SocialTeam"
    component_config_schema = SocialGroupChatConfig

    def __init__(
        self,
        participants: List[ChatAgent],
        *,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = 20,
        runtime: AgentRuntime | None = None,
        custom_message_types: List[type[BaseAgentEvent | BaseChatMessage]]
        | None = None,
    ) -> None:
        # self.session_id = get_chat_session_id_ctx() or generate_uuid()

        super().__init__(
            participants,
            group_chat_manager_name="SocialTeamManager",
            group_chat_manager_class=SocialTeamManager,
            termination_condition=termination_condition,
            max_turns=max_turns,
            runtime=runtime,
            custom_message_types=custom_message_types,
        )

    def _create_group_chat_manager_factory(
        self,
        name: str,
        group_topic_type: str,
        output_topic_type: str,
        participant_topic_types: List[str],
        participant_names: List[str],
        participant_descriptions: List[str],
        output_message_queue: asyncio.Queue[
            BaseAgentEvent | BaseChatMessage | GroupChatTermination
        ],
        termination_condition: TerminationCondition | None,
        max_turns: int | None,
        message_factory: MessageFactory,
    ) -> Callable[[], SocialTeamManager]:
        def _factory() -> SocialTeamManager:
            return SocialTeamManager(
                name=name,
                group_topic_type=group_topic_type,
                output_topic_type=output_topic_type,
                participant_topic_types=participant_topic_types,
                participant_names=participant_names,
                participant_descriptions=participant_descriptions,
                output_message_queue=output_message_queue,
                termination_condition=termination_condition,
                max_turns=max_turns,
                message_factory=message_factory,
            )

        return _factory

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
                    topic=topic,
                    source=source,
                    type=StateType.RUNTIMESTATE.value,
                    chatId=self.session_id,
                    state=v,
                ),
            )

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._runtime.load_state(state)

    async def load_runtimestate(self, session_id: str, runtime: AgentRuntime) -> None:
        state_list = await self.tenant_client.ag_state_api.ag_state_list(
            tenant=self.tenant_client.tenant_id,
            session=session_id,
        )

        state_dict = {}
        for state in state_list.rows:
            key = f"{state.topic}/{state.source}"
            state_dict[key] = state.state
        await runtime.load_state(state_dict)

    def _to_config(self) -> SocialTeamConfig:
        return SocialTeamConfig(
            max_turns=self._max_turns,
        )

    @classmethod
    def _from_config(cls, config: SocialTeamConfig) -> Self:
        model_client = get_default_model_client()
        participants = [
            AssistantAgent(
                name="assisant",
                description="an useful assistant.",
                system_message=dedent(
                    "你是实用助手,需要使用提供的工具解决用户提出的问题"
                    "重要:"
                    "1. 当用户明确调用 登录工具时才调用 登录工具"
                    "2. 当用户明确调用 获取天气工具时才调用 获取天气工具"
                ),
                model_client=model_client,
            )
        ]
        return cls(
            participants,
            # termination_condition=termination_condition,
            max_turns=config.max_turns,
        )

    async def _from_db_config(self, config: any) -> Self:
        pass

    async def pause(self) -> None:
        logger.info("TODO: pause team")

    async def resume(self) -> None:
        logger.info("TODO: resume team")
