import time
import logging
from autogen_core import Component, DefaultTopicId, MessageContext, RoutedAgent, TopicId, default_subscription, message_handler
from autogen_agentchat.agents._user_proxy_agent import UserProxyAgentConfig
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
)
from ..mtlibs.id import generate_uuid
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from mtmaisdk.clients.rest.models.chat_message_create import ChatMessageCreate
from mtmaisdk.clients.rest_client import AsyncRestApi
from pydantic import BaseModel
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult, Team
from typing import Callable, Optional, Union
from autogen_core import CancellationToken, Component, ComponentModel
from pathlib import Path
from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

logger = logging.getLogger(__name__)

@default_subscription
class WorkerMainAgent(RoutedAgent):
    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        super().__init__("WorkerMainAgent")
        self.gomtmapi=gomtmapi

    async def _create_team(
        self,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
    ) -> Component:
        """Create team instance from config"""
        # Handle different input types
        if isinstance(team_config, (str, Path)):
            config = await self.load_from_file(team_config)
        elif isinstance(team_config, dict):
            config = team_config
        else:
            config = team_config.model_dump()

        # Use Component.load_component directly
        team = Team.load_component(config)

        for agent in team._participants:
            if hasattr(agent, "input_func"):
                agent.input_func = input_func

        # TBD - set input function
        return team

    async def run_stream(
        self,
        input: AgentRunInput,
        input_func: Optional[Callable] = None,
        cancellation_token: Optional[CancellationToken] = None,
    ):
        start_time = time.time()
        team_data = await self.gomtmapi.teams_api.team_get(
            tenant=input.tenant_id, team=input.team_id
        )
        if team_data is None:
            raise ValueError("team not found")

        team = await self._create_team(team_data.component)
        try:
            async for event in team.run_stream(
                task=input.content,
            ):
                if cancellation_token and cancellation_token.is_cancelled():
                    break
                else:
                    yield event
            state_to_save = await team.save_state()
            # 保存状态
            saveed_response = (
                await self.gomtmapi.ag_state_api.ag_state_upsert(
                    tenant=input.tenant_id,
                    state=input.team_id,
                    ag_state_upsert=AgStateUpsert(
                        # id=team_id,
                        # version=state_to_save.get("version"),
                        state=state_to_save,
                        # type=state_to_save.get("type"),
                    ),
                )
            )
            logger.info(f"saveed_response: {saveed_response}")
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise e
        finally:
            # Ensure cleanup happens
            if team and hasattr(team, "_participants"):
                for agent in team._participants:
                    if hasattr(agent, "close"):
                        await agent.close()

    @message_handler
    async def on_new_message(self, message: AgentRunInput, ctx: MessageContext) -> None:
        logger.info(f"WorkerMainAgent 收到消息: {message}")

        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            await self.runtime.publish_message(
                    input,
                    topic_id=TopicId(type="tenant", source="tenant"),
                )
            return

        thread_id= message.session_id
        if not thread_id:
            thread_id=generate_uuid()
        async for event in self.run_stream(input=message):
            if isinstance( event, TextMessage) or isinstance(event, TaskResult):
                await self.publish_message(
                    topic_id=DefaultTopicId(),
                    message=ChatMessageCreate(
                        content=event.content,
                        tenant_id=message.tenant_id,
                        team_id=message.team_id,
                        threadId=thread_id,
                        runId=message.run_id,
                    ),
                )
            elif isinstance(event, BaseModel):
                await self.publish_message(
                    # todo 消息content 需要正确处理
                    message=ChatMessageCreate(content=event.model_dump_json(), tenant_id=message.tenant_id, team_id=message.team_id),
                    topic_id=DefaultTopicId(),
                )
                await self.gomtmapi.ag_events_api.ag_event_create(
                    tenant=message.tenant_id,
                    ag_event_create=AgEventCreate(
                        data=event,
                        framework="autogen",
                        # stepRunId=hatctx.step_run_id,
                        meta={},
                    ),
                )
            else:
                logger.info(f"WorkerMainAgent 收到消息: {event}")


    async def action_seed_tenant(self, message: AgentRunInput):
        logger.info(f"WorkerMainAgent 收到消息: {message}")
        pass
