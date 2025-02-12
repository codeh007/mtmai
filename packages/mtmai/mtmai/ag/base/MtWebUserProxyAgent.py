import logging

from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.agents._user_proxy_agent import UserProxyAgentConfig
logger = logging.getLogger(__name__)


class MtWebUserProxyAgent(UserProxyAgent):
    """扩展 UserProxyAgent"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _to_config(self) -> UserProxyAgentConfig:
        # TODO: Add ability to serialie input_func
        return UserProxyAgentConfig(name=self.name, description=self.description, input_func=None)