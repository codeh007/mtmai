import httpx
from mtmpb import events_connecpy

from mtmai.mtmpb import ag_connecpy


class MtmClient:
    """
    MTM 客户端
    参考: https://github.com/i2y/connecpy/blob/main/example/async_client.py
    """

    def __init__(self, url: str, timeout_s: int = 20):
        self.session = httpx.AsyncClient(
            base_url=url,
            timeout=timeout_s,
        )
        self.ag = ag_connecpy.AsyncAgServiceClient(
            url, session=self.session, timeout=timeout_s
        )
        self.events = events_connecpy.AsyncEventsServiceClient(
            url, session=self.session, timeout=timeout_s
        )
