from langchain_core.runnables import RunnableConfig

from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState
import structlog

LOG = structlog.get_logger()



class HumanInputNode:
    def __init__(self):
        pass

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        LOG.info("进入 HumanInputNode ")
        messages = state.messages
        user_input = state.user_input
        if user_input == "/1":
            LOG.info("特殊指令1")
            return {
                "next": "articleGen"
            }

        if user_input == "/2":
            LOG.info("特殊指令2")
            return {
                "next": "site"
            }
        return {
            "messages": messages,
            "next": "assistant",
        }
