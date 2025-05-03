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
        self.connect()

    def connect(self):
        ws_url = f"{http_url_ws(settings.WORKER_GATEWAY_URL)}/api/chat/default"
        logger.info(f"连接到 {ws_url}")
        max_retry = 10
        retry_interval = 5
        retry_count = 0

        while retry_count < max_retry:
            try:
                with connect(ws_url) as websocket:
                    retry_count = 0  # 重置重试计数
                    while True:
                        try:
                            message = websocket.recv()
                            json_message = json.loads(message)
                            msg_type = json_message["type"]
                            if msg_type == "cf_agent_state":
                                logger.info(json_message)
                            elif msg_type == "connected":
                                self.on_connected(websocket, json_message)
                            else:
                                logger.error(f"未知的消息类型: {msg_type}")
                        except Exception as e:
                            logger.error(f"处理消息时出错: {e}")
                            break

            except Exception as e:
                retry_count += 1
                logger.error(f"WebSocket连接失败 (尝试 {retry_count}/{max_retry}): {e}")
                if retry_count < max_retry:
                    import time

                    time.sleep(retry_interval)
                else:
                    logger.error("达到最大重试次数,退出重连")
                    break

    def on_connected(self, ws, msg):
        logger.info("WebSocket连接成功")
        ws.send(json.dumps({"type": "worker_init", "worker_id": "1234567890"}))
