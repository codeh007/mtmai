import asyncio
import os
from contextlib import asynccontextmanager
from typing import Optional

import click
import typer
from fastapi import FastAPI
from loguru import logger

import mtmai.core.bootstraps as bootstraps
from mtmai.core.config import settings

bootstraps.bootstrap_core()
app = typer.Typer(invoke_without_command=True)


os.environ["DISPLAY"] = ":1"


@app.callback()
def main(ctx: typer.Context):
    # 如果没有指定子命令，默认执行 serve 命令
    if ctx.invoked_subcommand is None:
        ctx.invoke(run)


@app.command()
def run():
    logger.info("mtm app starting ...")
    pwd = os.path.dirname(os.path.abspath(__file__))
    agents_dir = os.path.join(pwd, "agents")
    web(agents_dir)


@app.command()
def web(
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
            f"""ADK Web Server started at http://localhost:{port}.{" "*(29 - len(str(port)))}""",
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

    # from mtmai.api.adk_fast_api import get_fast_api_app

    # app = get_fast_api_app(
    #     agent_dir=agents_dir,
    #     # session_db_url=session_db_url,
    #     session_db_url="",
    #     # allow_origins=allow_origins,
    #     web=True,
    #     trace_to_cloud=trace_to_cloud,
    #     lifespan=_lifespan,
    # )
    # app = FastAPI()

    # Add MCP server to the FastAPI app
    # mcp = FastApiMCP(app)
    # mcp.mount()

    # config = uvicorn.Config(
    #     app,
    #     host="0.0.0.0",
    #     port=port,
    #     reload=True,
    # )

    # server = uvicorn.Server(config)
    # server.run()

    from mtmai.server import serve

    asyncio.run(serve())


if __name__ == "__main__":
    app()
