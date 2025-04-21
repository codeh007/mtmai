import json

from loguru import logger
from websockets.sync.client import connect

from mtmai.core.config import settings
from mtmai.mtlibs.utils import http_url_ws


class WSAgentWorker:
    """基于 web socket 的worker"""

    def __init__(self):
        self.ws_client = None

    def start(self):
        self.connect_root()

    def connect_root(self):
        self.root_ws_url = (
            f"{http_url_ws(settings.WORKER_GATEWAY_URL)}/agents/root-ag/default"
        )
        with connect(self.root_ws_url) as websocket:
            message = websocket.recv()
            json_message = json.loads(message)
            msg_type = json_message["type"]
            if msg_type == "cf_agent_state":
                logger.info(json_message)
                self.root_state = json_message["state"]
            else:
                logger.error(f"未知的消息类型: {msg_type}")

    def connect(self):
        ws_url = f"{http_url_ws(settings.WORKER_GATEWAY_URL)}/agents/chat/chat-2"
        with connect(ws_url) as websocket:
            message = websocket.recv()
            # logger.info(f"收到消息: {message}")
            json_message = json.loads(message)
            msg_type = json_message["type"]
            if msg_type == "cf_agent_state":
                logger.info(json_message)
            else:
                logger.error(f"未知的消息类型: {msg_type}")
