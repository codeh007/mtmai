import asyncio
import os
from typing import Annotated

import typer
from loguru import logger

from mtmai.core import bootstrap_core
from mtmai.core.config import settings

bootstrap_core()
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
    serve(agents_dir)


@app.command()
def serve(
    host: Annotated[
        str,
        typer.Option("--host", "-h", help="Host to bind the server to"),
    ] = "0.0.0.0",
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Port to bind the server to"),
    ] = settings.PORT,
    enable_worker: Annotated[
        bool,
        typer.Option("--enable-worker", "-w", help="Enable worker"),
    ] = True,
):
    from mtmai.server import MtmaiServeOptions, serve

    asyncio.run(
        serve(
            MtmaiServeOptions(
                host=host,
                port=port,
                enable_worker=enable_worker,
            )
        )
    )


@app.command()
def wsworker():
    from mtmai.ws_worker import WSAgentWorker

    asyncio.run(WSAgentWorker().start())


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
uv sync
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
    # typer.run(main)
