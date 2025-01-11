import asyncio
import logging
import os
import sys

from dotenv import load_dotenv


def bootstrap_core():
    from .config import settings
    from .logging import setup_logging

    load_dotenv()
    setup_logging()
    logger = logging.getLogger()
    logger.info(
        f"[🚀🚀🚀 mtmai]({settings.VERSION})"  # noqa: G004
    )
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # setup http proxy
    if settings.HTTP_PROXY:
        logger.info(f"HTTP_PROXY: {settings.HTTP_PROXY}")
        os.environ["HTTP_PROXY"] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        logger.info(f"HTTPS_PROXY: {settings.HTTPS_PROXY}")
        os.environ["HTTPS_PROXY"] = settings.HTTPS_PROXY
    if settings.SOCKS_PROXY:
        logger.info(f"SOCKS_PROXY: {settings.SOCKS_PROXY}")
        os.environ["SOCKS_PROXY"] = settings.SOCKS_PROXY
