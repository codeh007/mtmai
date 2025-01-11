import os
from urllib.parse import urlparse

from mtmaisdk.utils.env import is_in_docker, is_in_testing, is_in_vercel


def is_in_dev() -> bool:
    """是否处于开发环境"""
    from mtmai.core.config import settings

    if is_in_gitpod():
        return True
    return (
        not is_in_docker()
        and not is_in_vercel()
        and not is_in_testing()
        and not settings.is_production
    )


def backend_url_base() -> str:
    from mtmai.core.config import settings

    if settings.Serve_ADDR:
        return f"http://{settings.Serve_ADDR}"

    gitpod_workspace_url = os.environ.get("GITPOD_WORKSPACE_URL")

    if gitpod_workspace_url:
        uri1 = urlparse(gitpod_workspace_url)
        return f"https://{settings.PORT}-{uri1.hostname}"
    return f"http://localhost:{settings.PORT}"


def get_server_host():
    gitpod_workspace_url = os.environ.get("GITPOD_WORKSPACE_URL")
    if gitpod_workspace_url:
        uri1 = urlparse(gitpod_workspace_url)
        return uri1.hostname
    return "0.0.0.0"  # noqa: S104


# def abs_url(req: Request, path_name: str = ""):
#     """
#     获取完整后端url, (自动处理反代的情况)
#     """
#     x_forwardd_host = req.headers.get("x-forwarded-host")
#     logger = getLogger()
#     logger.info("获取绝对网址, headers:", req.headers)
#     base_url = backend_url_base()
#     if x_forwardd_host:
#         # x_forwardd_port = req.headers.get("x-forwarded-port")
#         x_forwardd_proto = req.headers.get("x-forwarded-proto")
#         base_url = f"{x_forwardd_proto}://{x_forwardd_host}"

#     return f"{base_url}{path_name}"


def is_in_gitpod() -> bool:
    return os.getenv("GITPOD_WORKSPACE_URL")
