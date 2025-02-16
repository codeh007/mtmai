import logging

from autogen_core import MessageContext, default_subscription, message_handler

from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert

from ._agents import MtBaseAgent

logger = logging.getLogger(__name__)


@default_subscription
class HfSpaceAgent(MtBaseAgent):
    """
    HfSpaceAgent 是 HfSpace 和 Worker 之间的桥梁, 负责处理 HfSpace 发送的消息,
    """

    # def __init__(self, wfapp: Hatchet = None) -> None:
    #     super().__init__("UI Agent")
    #     if wfapp is not None:
    #         self.wfapp = wfapp
    #         self.gomtmapi = self.wfapp.rest.aio

    @message_handler
    async def handle_message(
        self, message: ChatMessageUpsert, ctx: MessageContext
    ) -> None:
        logger.info(f"HFSpace 收到消息:{self.type}")
