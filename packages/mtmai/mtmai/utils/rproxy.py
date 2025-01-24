import logging

# from urllib.parse import urlparse
# import httpx
from fastapi import APIRouter
from opentelemetry import trace

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()

serve_prefix = "/rproxy"
target_url_base = "http://www.xinhuanet.com"


# @router.api_route(
#     serve_prefix + "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
# )
# async def proxy(request: Request):
#     target_path = request.url.path[len(serve_prefix) :]

#     target_url = f"{target_url_base}{target_path}"
#     logger.info("rproxy => %s", target_url)

#     parsed_url = urlparse(target_url_base)
#     host = parsed_url.hostname

#     headers = dict(request.headers)
#     headers["host"] = host  # 必须小写

#     try:
#         async with httpx.AsyncClient() as client:
#             proxy_response = await client.request(
#                 method=request.method,
#                 url=target_url,
#                 headers=headers,
#                 content=await request.body(),
#             )
#             headers = dict(proxy_response.headers)
#             headers.pop("content-length", None)
#             headers.pop("content-encoding", None)
#             headers.pop("connection", None)
#             return Response(
#                 content=proxy_response.content,
#                 status_code=proxy_response.status_code,
#                 headers=headers,
#             )
#     except Exception as e:
#         return Response(
#             content=f"Request Error: {e}",
#             status_code=500,
#         )
