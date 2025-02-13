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
from mtmaisdk.clients.rest.models.chat_message import ChatMessage
from mtmaisdk.clients.rest.models.chat_message_create import ChatMessageCreate
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

    @message_handler
    async def handle_message_chunk(self, message: ChatMessageCreate, ctx: MessageContext) -> None:
        logger.info(f"UI Agent 收到消息: {message}")

        # 聊天消息入库功能暂时取消,因后端没完全实现()
        # await self.gomtmapi.chat_api.chat_create_message(
        #     tenant=message.tenant_id,
        #     chat_message_create=message,
        #     )

        # 保存状态
        state = await self.runtime.save_state()
        logger.info(f"UI Agent 保存状态: {state}")


        # 保存 跟用户的聊天信息
        try:
            chatSession=self.gomtmapi.chat_api.chat_session_get(
                tenant_id=message.tenant_id,
                session_id=message.session_id,
            )
        except Exception as e:
            logger.error(f"UI Agent 获取聊天 Session 失败: {e}")




    async def save_state(self) -> Mapping[str, Any]:
        """Save the state of the group chat team."""
        try:
            # Save the state of the runtime. This will save the state of the participants and the group chat manager.
            # agent_states = await self._runtime.save_state()
            # return TeamState(agent_states=agent_states, team_id=self._team_id).model_dump()

            return UIAgentState(last_message="last_message:todo").model_dump()
        finally:
            # Indicate that the team is no longer running.
            # self._is_running = False
            pass

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        self.last_message = state["last_message"]
