import asyncio
import logging
import os
import sys
import warnings
from pathlib import Path

from dotenv import load_dotenv

# 忽略 Pydantic 的特定警告
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Field name.*shadows an attribute in parent.*",
)


is_bootstraped = False
default_env_files = [
    ".env",
    ".env.local",
    "../gomtm/env/dev.env",
    "../../gomtm/env/dev.env",
    "../../../gomtm/env/dev.env",
]
# load_dotenv(override=True)
for env_file in default_env_files:
    env_path = Path(env_file).absolute()
    if env_path.exists():
        load_dotenv(env_path, override=True)


def bootstrap_core():
    global is_bootstraped
    if is_bootstraped:
        return
    is_bootstraped = True

    from mtmai._version import version

    from .logging import setup_logging

    logger = logging.getLogger()

    setup_logging()
    logger.info(
        f"[🚀🚀🚀 mtmai]({version})"  # noqa: G004
    )
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # if settings.HTTP_PROXY:
    #     logger.info(f"HTTP_PROXY: {settings.HTTP_PROXY}")
    #     os.environ["HTTP_PROXY"] = settings.HTTP_PROXY
    # if settings.HTTPS_PROXY:
    #     logger.info(f"HTTPS_PROXY: {settings.HTTPS_PROXY}")
    #     os.environ["HTTPS_PROXY"] = settings.HTTPS_PROXY
    # if settings.SOCKS_PROXY:
    #     logger.info(f"SOCKS_PROXY: {settings.SOCKS_PROXY}")
    #     os.environ["SOCKS_PROXY"] = settings.SOCKS_PROXY

    os.environ["DISPLAY"] = ":1"
