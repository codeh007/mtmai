import logging

from autogen_agentchat.teams import RoundRobinGroupChat

logger = logging.getLogger(__name__)


class MtRoundRobinGroupChat(RoundRobinGroupChat):
    """RoundRobinGroupChat"""
