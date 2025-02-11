import logging

from autogen_agentchat.agents import UserProxyAgent

logger = logging.getLogger(__name__)


class MtWebUserProxyAgent(UserProxyAgent):
    """扩展 UserProxyAgent"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
