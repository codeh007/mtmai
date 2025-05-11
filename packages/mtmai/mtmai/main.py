import asyncio
import os
from contextlib import asynccontextmanager
from typing import Optional

import click
import typer
import uvicorn
from fastapi import FastAPI
from loguru import logger

from mtmai.core import bootstraps
from mtmai.core.config import settings

bootstraps.bootstrap_core()
app = typer.Typer(invoke_without_command=True)


@app.callback()
def main(ctx: typer.Context):
    # 默认执行 serve 命令
    if ctx.invoked_subcommand is None:
        ctx.invoke(serve)


@app.command()
def run():
    logger.info("mtm app starting ...")
    pwd = os.path.dirname(os.path.abspath(__file__))
    agents_dir = os.path.join(pwd, "agents")
    adkweb(agents_dir)


@app.command()
def serve():
    from mtmai.server import serve

    asyncio.run(serve())


@app.command()
def wsworker():
    from mtmai.ws_worker import WSAgentWorker

    asyncio.run(WSAgentWorker().start())


@app.command()
def worker():
    from mtmai.worker_v2 import WorkerV2

    asyncio.run(
        WorkerV2(
            db_url=settings.MTM_DATABASE_URL,
        ).start_block()
    )


@app.command()
def adkweb(
    agents_dir: str,
    log_to_tmp: bool = True,
    # session_db_url: str = settings.SESSION_DB_URL,
    session_db_url: str = settings.MTM_DATABASE_URL,
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
    port: int = settings.PORT,
    trace_to_cloud: bool = False,
):
    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        # from mtmai.worker_app import run_worker
        # worker_task = asyncio.create_task(run_worker())

        click.secho(
            f"""ADK Web Server started at http://localhost:{port}.{" " * (29 - len(str(port)))}""",
            fg="green",
        )
        yield  # Startup is done, now app is running

        # Cleanup worker on shutdown
        # if not worker_task.done():
        #     worker_task.cancel()
        #     try:
        #         await worker_task
        #     except asyncio.CancelledError:
        #         pass

        click.secho(
            """ADK Web Server shutting down... """,
            fg="green",
        )

    from mtmai.api.adk_web_api import configure_adk_web_api

    app = configure_adk_web_api(
        agent_dir=agents_dir,
        # session_db_url=session_db_url,
        session_db_url="",
        # allow_origins=allow_origins,
        web=True,
        trace_to_cloud=trace_to_cloud,
        lifespan=_lifespan,
    )

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=port,
        reload=True,
    )

    server = uvicorn.Server(config)
    server.run()

    # from mtmai.server import serve

    # asyncio.run(serve())


@app.command()
def chrome():
    asyncio.run(start_chrome_server())


async def start_chrome_server():
    cmd = "google-chrome "
    "--remote-debugging-port=15001"
    ("--disable-dev-shm-usage",)
    ("--no-first-run",)
    ("--no-default-browser-check",)
    ("--disable-infobars",)
    ("--window-position=0,0",)
    ("--disable-session-crashed-bubble",)
    ("--hide-crash-restore-bubble",)
    ("--disable-blink-features=AutomationControlled",)
    ("--disable-automation",)
    ("--disable-webgl",)
    ("--disable-webgl2",)
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        print("Chrome debugging server started on port 15001. Press Ctrl+C to exit...")
        await process.communicate()
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, shutting down Chrome...")
        process.terminate()
        await process.wait()


@app.command()
def mcpserver():
    import asyncio

    from mtmai.mcp_server.mcp_app import mcpApp

    logger.info(f"Starting MCP server on http://localhost:{settings.PORT}")
    asyncio.run(
        mcpApp.run_sse_async(
            host="0.0.0.0",
            port=settings.PORT,
        )
    )


@app.command()
def setup():
    install1 = "sudo apt install -yqq ffmpeg imagemagick"
    os.system(install1)

    os.system("apt-get install -y libpq-dev")

    # 修正 ImageMagick 安全策略, 允许读写
    cmd = "sudo sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml"
    os.system(cmd)

    commamd_line = """
uv sync
# 原因: crawl4ai 库本本项目有冲突,所以使用独立的方式设置
uv pip install crawl4ai f2 --no-deps

# 原因: moviepy 库 引用了  pillow <=11
uv pip install "moviepy>=2.1.2" --no-deps

uv add playwright_stealth

uv pip install google-generativeai~=0.8.3
uv pip install torch
"""
    os.system(commamd_line)


@app.command()
def download_models():
    from mtmai.mtlibs.hf_utils.hf_utils import download_whisper_model

    # 相对当前文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_whisper_model(
        os.path.join(current_dir, "mtlibs/NarratoAI/app/models/faster-whisper-large-v2")
    )


if __name__ == "__main__":
    app()
