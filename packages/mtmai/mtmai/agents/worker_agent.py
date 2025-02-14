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

from mtmaisdk.clients.rest.models.ag_state import AgState

from ..aghelper import AgHelper

from .team_builder.assisant_team_builder import AssistantTeamBuilder
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

deault_team_label = "default"

@default_subscription
class WorkerMainAgent(RoutedAgent):
    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        super().__init__("WorkerMainAgent")
        self.gomtmapi=gomtmapi

    async def _create_team_component(
        self,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
    ) -> Component:
        """Create team instance from config"""
        if isinstance(team_config, (str, Path)):
            config = await self.load_from_file(team_config)
        elif isinstance(team_config, dict):
            config = team_config
        else:
            config = team_config.model_dump()

        team = Team.load_component(config)

        for agent in team._participants:
            if hasattr(agent, "input_func"):
                agent.input_func = input_func

        return team

    @message_handler
    async def on_new_message(self, message: AgentRunInput, ctx: MessageContext) -> None:
        start_time = time.time()
        logger.info(f"WorkerMainAgent 收到消息: {message}")

        ag_helper = AgHelper(self.gomtmapi)
        if not message.team_id:
            team = await ag_helper.get_or_create_default_team(
                tenant_id=message.tenant_id,
                label=deault_team_label,
            )
            message.team_id = team.metadata.id
        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            await self.runtime.publish_message(
                    message,
                    topic_id=TopicId(type="tenant", source="tenant"),
                )
            return

        thread_id= message.session_id
        if not thread_id:
            thread_id=generate_uuid()

        team_component_data:Component = None
        if not message.team_id:
            # 获取模型配置
            defaultModel = await self.gomtmapi.model_api.model_get(
                tenant=input.tenant_id, model="default"
            )
            model_config = defaultModel.config
            default_team_builder = AssistantTeamBuilder()
            team_component = await default_team_builder.create_team(model_config)
            team_component_data=team_component.dump_component()
        else:
            team_data = await self.gomtmapi.teams_api.team_get(
                tenant=message.tenant_id, team=message.team_id
            )
            if team_data is None:
                raise ValueError("team not found")
            team_component_data=team_data.component
        team = await self._create_team_component(team_component_data)

        component=team
        team_id=message.team_id
        if not team_id:
            team_id=generate_uuid()
        try:
            async for event in component.run_stream(
                task=message.content,
                cancellation_token=ctx.cancellation_token,
            ):
                if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
                    break
                try:
                    if isinstance(event, TaskResult):
                        # await self.publish_message(
                        #     topic_id=DefaultTopicId(),
                        #     message=ChatMessageCreate(
                        #         content=event.messages[],
                        #         tenant_id=message.tenant_id,
                        #         team_id=message.team_id,
                        #         threadId=thread_id,
                        #         runId=message.run_id,
                        #     ),
                        # )
                        logger.info(f"WorkerMainAgent TaskResult: {event}")
                    elif isinstance( event, TextMessage):
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
                        logger.info(f"WorkerMainAgent 收到(未知类型)消息: {event}")
                except Exception as e:
                    logger.error(f"WorkerMainAgent stream 运行出错: {e}")

        except Exception as e:
            logger.error(f"WorkerMainAgent 运行出错: {e}")
        finally:
            # 保存状态
            if team and hasattr(team, "_participants"):
                for agent in team._participants:
                    if hasattr(agent, "close"):
                        await agent.close()
            try:
                state_to_save = await team.save_state()
                saveed_response: AgState = (
                    await self.gomtmapi.ag_state_api.ag_state_upsert(
                        tenant=message.tenant_id,
                        state=thread_id,
                        ag_state_upsert=AgStateUpsert(
                            id=thread_id,
                            componentId=team_id,
                            runId=message.run_id,
                            state=state_to_save,
                        ),
                    )
                )
                # logger.info(f"WorkerMainAgent 保存状态: {saveed_response}")
            except Exception as e:
                logger.error(f"WorkerMainAgent 保存状态出错: {e}")

    async def action_seed_tenant(self, message: AgentRunInput):
        logger.info(f"WorkerMainAgent 收到消息: {message}")
