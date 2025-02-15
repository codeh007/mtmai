import logging
from typing import Any, Awaitable, Callable, List, Mapping
from autogen_core import  MessageContext, RoutedAgent, default_subscription, message_handler
from ..mtmaisdk.hatchet import Hatchet
from ..mtmaisdk.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from ..mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert
from ._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from ..mtmaisdk.clients.rest.models.task_result import TaskResult
from ..mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from ..mtmaisdk.clients.rest.exceptions import ApiException

logger = logging.getLogger(__name__)
@default_subscription
class UIAgent(RoutedAgent):
    """
    UI Agent 是 UI 和 Worker 之间的桥梁, 负责处理 UI 发送的消息,
        1: 将状态通过SSE 推送到web 前端,
        2: 将消息和状态持久化到数据库
    """

    def __init__(self, wfapp: Hatchet) -> None:
        super().__init__("UI Agent")
        self.wfapp = wfapp
        self.gomtmapi = self.wfapp.rest.aio

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        self.last_message = state["last_message"]

    @message_handler
    async def handle_message_create(self, message: ChatMessageUpsert, ctx: MessageContext) -> None:
        # logger.info(f"UI Agent 收到消息: {message}")
        try:
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
        # tenant_id=get_tenant_id()
        logger.info(f"TODO: AgEventCreate")

    @message_handler
    async def handle_task_result(self, message: TaskResult, ctx: MessageContext) -> None:
        logger.info(f"TODO: TaskResult")

    @message_handler
    async def handle_api_save_team_state(self, message: ApiSaveTeamState, ctx: MessageContext) -> None:
        """保存团队状态"""
        logger.info(f"保存团队状态")
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
        logger.info(f"TODO:UI Agent 保存任务结果")
