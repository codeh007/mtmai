import httpx

from mtmai.mtmpb import ag_connecpy


class MtmClient:
    def __init__(self, url: str, timeout_s: int = 20):
        self.session = httpx.AsyncClient(
            base_url=url,
            timeout=timeout_s,
        )
        self.ag = ag_connecpy.AsyncAgServiceClient(url, session=self.session)
