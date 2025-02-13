import logging
from typing import List
from autogen_core import Component, DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_agentchat.agents._user_proxy_agent import UserProxyAgentConfig
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
)
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from mtmaisdk.clients.rest.models.chat_message_create import ChatMessageCreate
from mtmaisdk.clients.rest_client import AsyncRestApi
from pydantic import BaseModel
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult, Team

from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from .team_runner import TeamRunner


@default_subscription
class WorkerMainAgent(RoutedAgent):
    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        super().__init__("WorkerMainAgent")
        self.gomtmapi=gomtmapi

    # @message_handler
    # async def on_new_message(self, message: CascadingMessage, ctx: MessageContext) -> None:
    #     """仅作练习"""
    #     logger.info(f"WorkerMainAgent 收到消息: {message}")
    #     await self.publish_message(
    #         ReceiveMessageEvent(round=message.round, sender=str(ctx.sender), recipient=str(self.id)),
    #         topic_id=DefaultTopicId(),
    #     )
    #     await self.publish_message(CascadingMessage(round=message.round + 1), topic_id=DefaultTopicId())


    @message_handler
    async def on_new_message(self, message: AgentRunInput, ctx: MessageContext) -> None:
        logger.info(f"WorkerMainAgent 收到消息: {message}")
        team_runner = TeamRunner(self.gomtmapi)
        async for event in team_runner.run_stream(input=message):
            if isinstance( event, TextMessage) or isinstance(event, TaskResult):
                await self.publish_message(
                    topic_id=DefaultTopicId(),
                    message=ChatMessageCreate(
                        content=event.content,
                        tenant_id=message.tenant_id,
                        team_id=message.team_id,
                        thread_id=message.thread_id,
                        run_id=message.run_id,
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