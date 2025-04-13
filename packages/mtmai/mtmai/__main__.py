import os
from contextlib import asynccontextmanager
from typing import Optional

import click
import typer
import uvicorn
from fastapi import FastAPI
from loguru import logger

import mtmai.core.bootstraps as bootstraps
from mtmai.core.config import settings

bootstraps.bootstrap_core()
app = typer.Typer(invoke_without_command=True)


@app.callback()
def main(ctx: typer.Context):
    # 如果没有指定子命令，默认执行 serve 命令
    if ctx.invoked_subcommand is None:
        ctx.invoke(run)


@app.command()
def run():
    logger.info("running worker")

    # 启动web 但是不阻塞

    pwd = os.path.dirname(os.path.abspath(__file__))
    agents_dir = os.path.join(pwd, "agents")
    web(agents_dir)
    # asyncio.run(run_worker())


@app.command()
def web(
    agents_dir: str,
    log_to_tmp: bool = True,
    session_db_url: str = settings.SESSION_DB_URL,
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
    port: int = settings.PORT,
    trace_to_cloud: bool = False,
):
    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        click.secho(
            f"""\
    +-----------------------------------------------------------------------------+
    | ADK Web Server started                                                      |
    |                                                                             |
    | For local testing, access at http://localhost:{port}.{" "*(29 - len(str(port)))}|
    +-----------------------------------------------------------------------------+
    """,
            fg="green",
        )
        yield  # Startup is done, now app is running
        click.secho(
            """\
    +-----------------------------------------------------------------------------+
    | ADK Web Server shutting down...                                             |
    +-----------------------------------------------------------------------------+
    """,
            fg="green",
        )

    from mtmai.api.adk_fast_api import get_fast_api_app

    app = get_fast_api_app(
        agent_dir=agents_dir,
        session_db_url=session_db_url,
        allow_origins=allow_origins,
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


if __name__ == "__main__":
    app()
