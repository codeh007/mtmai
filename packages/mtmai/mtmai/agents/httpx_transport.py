import logging

import httpx

logger=logging.getLogger("httpx_transport")

class LoggingTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        response = await super().handle_async_request(request)
        # 提示： 不要读取 body，因为一般 是stream，读取了会破环状态
        logger.info(
            f"LLM http req:\n{str(request.content)}\nResponse: {response.status_code}\n {request.url}\n"
        )
        return response