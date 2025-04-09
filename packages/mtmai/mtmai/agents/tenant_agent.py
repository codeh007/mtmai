from typing import Any, Mapping

from autogen_agentchat.agents import AssistantAgent
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ChatCompletionClient
from loguru import logger
from mtmai.clients.rest.models.mt_component_upsert import MtComponentUpsert
from mtmai.clients.rest.models.tenant_init_input import TenantInitInput
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.mtlibs.id import generate_uuid


class TenantAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        session_id: str,
        model_client: ChatCompletionClient | None = None,
        user_agent_topic_type: str = None,
    ) -> None:
        super().__init__(description)
        self._user_agent_topic_type = user_agent_topic_type
        self._model_context = BufferedChatCompletionContext(buffer_size=10)
        self._session_id = session_id
        self.model_client = model_client
        # self.instagram_agent_id = AgentId(self._social_agent_topic_type, "default")
        self._delegate = AssistantAgent("user_agent", model_client=self.model_client)
        self.tenant_client = TenantClient()

    @message_handler
    async def handle_tenant_init(
        self, message: TenantInitInput, ctx: MessageContext
    ) -> None:
        """用户输入"""
        if ctx.cancellation_token.is_cancelled():
            return

        session_id = self.id.key
        logger.info(
            f"{'-'*80}\nhandle_tenant_init, session ID: {session_id}. task: {message.content}"
        )

        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        from mtmai.mtlibs.autogen_utils.gallery_builder import (
            create_default_gallery_builder,
        )

        gallery_builder = create_default_gallery_builder()
        gallery_id = generate_uuid()
        for component in gallery_builder.teams:
            mt_component_upsert = MtComponentUpsert(
                galleryId=gallery_id,
                label=component.label,
                description=component.description,
                version=component.version,
                component_version=component.component_version,
                provider=component.provider,
                component_type=component.component_type,
                config=component.config,
            )
            await self.tenant_client.coms_api.coms_upsert(
                tenant=tid,
                com=generate_uuid(),
                mt_component_upsert=mt_component_upsert.model_dump(),
            )
        return {
            "success": True,
        }

    async def save_state(self) -> Mapping[str, Any]:
        return {
            "model_context": await self._model_context.save_state(),
        }

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._model_context.load_state(state["model_context"])
        self.is_waiting_ig_login = state.get("is_waiting_ig_login", False)
