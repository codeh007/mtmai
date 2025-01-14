import logging
from pathlib import Path

from fastapi import APIRouter
from mtmai.core.config import settings
from mtmai.mtlibs.mtutils import command_exists

from mtmlib.httpUtils import download_file
from mtmlib.mtutils import bash

router = APIRouter()
logger = logging.getLogger()


async def start_cloudflared():
    if not settings.CF_TUNNEL_TOKEN:
        logger.warning("missing env CF_TUNNEL_TOKEN")
        return
    await install()
    bash("sudo pkill cloudflared || true")
    logger.info("----start up cloudflared tunnel----")
    bash(
        f"""cloudflared tunnel --no-autoupdate --http2-origin --no-chunked-encoding=false run --token {settings.CF_TUNNEL_TOKEN} & """
    )


async def install():
    if not command_exists("cloudflared"):
        logger.info("cloudflared 命令不存在现在安装")
        cloudflared_bin_path = str(Path.home() / ".local/bin/cloudflared")
        await download_file(
            "https://github.com/cloudflare/cloudflared/releases/download/2024.1.5/cloudflared-linux-amd64",
            cloudflared_bin_path,
        )
        bash(f"chmod +x {cloudflared_bin_path}")
    # return "installed"
