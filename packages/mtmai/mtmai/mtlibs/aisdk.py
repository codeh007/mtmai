"""
doc: https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol
"""

import json

from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse


def text(word: str):
    return f"0:{json.dumps(word)}\n"


def data(items):
    if isinstance(items, list):
        return f"2:{json.dumps(jsonable_encoder(items))}\n"
    else:
        return f"2:{json.dumps([jsonable_encoder(items)])}\n"


def error(error_message: str):
    return f"3:{json.dumps(error_message)}\n"


def finish(reason: str = "stop", prompt_tokens: int = 0, completion_tokens: int = 0):
    data = {
        "finishReason": reason,
        "usage": {"promptTokens": prompt_tokens, "completionTokens": completion_tokens},
    }
    return f"d:{json.dumps(data)}\n"


def AiSDKStreamResponse(content):
    """
    说明: 在 cloudflared tunnel 上，是支持 http sse 的，不需要特别添加 headers。
    例子：
    @router.get("/hello_stream1")
    async def hello_stream1():
        from fastapi.responses import StreamingResponse
        async def event_generator():
            for i in range(10):
                yield aisdk.text(f"Hello, this is message {i}")
                await asyncio.sleep(0.5)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    **注意** 如果加了多余的http header 可能导致 cloudflared tunnel 环境下无法正常工作。
    """
    return StreamingResponse(
        content,
        media_type="text/event-stream",
        # headers={
        #     "Cache-Control": "no-cache, no-transform, no-store, must-revalidate, proxy-revalidate",
        #     "x-vercel-ai-data-stream": "v1",
        #     "content-type": "text/plain; charset=utf-8",
        #     "vary": "RSC, Next-Router-State-Tree, Next-Router-Prefetch",
        #     "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate",
        #     "pragma": "no-cache",
        #     "expires": "0",
        #     "surrogate-control": "no-store",
        #     "Content-Type": "text/event-stream",
        #     "Connection": "keep-alive",
        #     "X-Accel-Buffering": "no",  # 用于 Nginx 代理
        #     "CF-Cache-Status": "DYNAMIC",  # 告诉 Cloudflare 这是动态内容
        #     "CF-Edge-Cache-Status": "DYNAMIC",  # 告诉 Cloudflare 这是动态内容
        #     "Transfer-Encoding": "chunked",  # 明确指定分块传输编码
        #     "X-Content-Type-Options": "nosniff",  # 防止内容类型嗅探
        # },
    )


# -------------------------------------------------------------------------
class AiTextChunck:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text
