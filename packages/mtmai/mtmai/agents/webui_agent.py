import logging
from typing import Any, Awaitable, Callable, List, Mapping
from autogen_core import  MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)

from ..mtmaisdk.clients.rest.models.chat_message_upsert import ChatMessageUpsert

from ..mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert


from ._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from ..mtmaisdk.clients.rest.models.task_result import TaskResult
from ..mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from ..context import get_tenant_id
from ..mtlibs.id import generate_uuid
from ..mtmaisdk.clients.rest.exceptions import ApiException
from mtmaisdk.clients.rest_client import AsyncRestApi
from rich.console import Console
from rich.markdown import Markdown
from pydantic import BaseModel


class UIAgentState(BaseModel):
    """UI Agent 状态"""
    last_message: str = ""


logger = logging.getLogger(__name__)
@default_subscription
class UIAgent(RoutedAgent):
    """Handles UI-related tasks and message processing for the distributed group chat system."""

    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        super().__init__("UI Agent")
        self.gomtmapi = gomtmapi

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        self.last_message = state["last_message"]

    @message_handler
    async def handle_message_create(self, message: ChatMessageUpsert, ctx: MessageContext) -> None:
        tenant_id=get_tenant_id()
        logger.info(f"UI Agent 收到消息: {message}")
        try:
            # chat_create_message 实际是 upsert
            await self.gomtmapi.chat_api.chat_message_upsert(
                tenant=message.tenant_id,
                chat_message_upsert=ChatMessageUpsert(
                    tenantId=message.tenant_id,
                    teamId=message.team_id,
                    content=message.content,
                    role=message.role,
                    threadId=message.thread_id,
                ).model_dump()
            )
        except ApiException as e:
            logger.error(f"UI Agent 保存消息失败: {e}")
            raise e
        except Exception as e:
            logger.error(f"UI Agent 保存消息失败(unknown error): {e}")
            raise e

    @message_handler
    async def handle_ag_event(self, message: AgEventCreate, ctx: MessageContext) -> None:
        tenant_id=get_tenant_id()
        logger.info(f"TODO: AgEventCreate {message}")

    @message_handler
    async def handle_task_result(self, message: TaskResult, ctx: MessageContext) -> None:
        logger.info(f"TODO: TaskResult {message}")

    @message_handler
    async def handle_api_save_team_state(self, message: ApiSaveTeamState, ctx: MessageContext) -> None:
        """保存团队状态"""
        logger.info(f"UI Agent 保存团队状态: {message}")
        try:
            await self.gomtmapi.ag_state_api.ag_state_upsert(
                    tenant=message.tenant_id,
                    ag_state_upsert=AgStateUpsert(
                        componentId=message.componentId,
                        runId=message.runId,
                        state=message.state,
                    ).model_dump(),
                )
        except Exception as e:
            logger.error(f"WorkerMainAgent 保存状态出错: {e}")

    @message_handler
    async def handle_api_save_team_task_result(self, message: ApiSaveTeamTaskResult, ctx: MessageContext) -> None:
        """保存团队最终结果"""
        logger.info(f"TODO:UI Agent 保存任务结果: {message}")
