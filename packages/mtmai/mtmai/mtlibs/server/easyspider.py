from pathlib import Path

from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmlib.mtutils import bash

logger = get_logger()
easy_spider_repo = "https://github.com/NaiboWang/EasySpider"

easy_targt_dir = str(Path(settings.storage_dir, "easyspider"))


def install_easy_spider():
    if not Path(easy_targt_dir).exists():
        bash(f"git clone {easy_spider_repo} {easy_targt_dir}")
    else:
        bash(f"cd {easy_targt_dir} && git pull")

    bash(f"cd {easy_targt_dir} && bun i")


def run_easy_spider_server():
    logger.info(f"启动 easy spider in {easy_targt_dir}")
    if not Path(easy_targt_dir).exists():
        logger.warning("⚠️ Easy Spider not installed, installing now...")
        install_easy_spider()
        return

    bash(f"cd {easy_targt_dir} && bun run server.js")


def run_easy_spider_ui():
    logger.info(f"启动 easy spider in {easy_targt_dir}")
    if not Path(easy_targt_dir).exists():
        logger.warning("⚠️ Easy Spider not installed, installing now...")
        install_easy_spider()
        return

    bash(f"cd {easy_targt_dir} && bun run start_direct")
