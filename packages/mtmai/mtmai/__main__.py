import asyncio
import os
from contextlib import asynccontextmanager
from typing import Optional

import click
import typer
import uvicorn
from fastapi import FastAPI
from loguru import logger

import mtmai.core.bootstraps as bootstraps

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
def host():
    asyncio.run(_run_ag_grpc_host())


async def _run_ag_grpc_host():
    import asyncio
    import platform

    from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost

    host = GrpcWorkerAgentRuntimeHost(address="localhost:7071")
    host.start()  # Start a host service in the background.
    if platform.system() == "Windows":
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await host.stop()
    else:
        await host.stop_when_signal()


@app.command()
def test_model_client():
    from mtmai.model_client.model_client import test_model_client2

    asyncio.run(test_model_client2(os.environ.get("OPENAI_API_KEY")))


@app.command()
# @click.option(
#     "--session_db_url",
#     help=(
#         "Optional. The database URL to store the session.\n\n  - Use"
#         " 'agentengine://<agent_engine_resource_id>' to connect to Vertex"
#         " managed session service.\n\n  - Use 'sqlite://<path_to_sqlite_file>'"
#         " to connect to a SQLite DB.\n\n  - See"
#         " https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls"
#         " for more details on supported DB URLs."
#     ),
# )
# @click.option(
#     "--port",
#     type=int,
#     help="Optional. The port of the server",
#     default=8000,
# )
# @click.option(
#     "--allow_origins",
#     help="Optional. Any additional origins to allow for CORS.",
#     multiple=True,
# )
# @click.option(
#     "--log_level",
#     type=click.Choice(
#         ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
#     ),
#     default="INFO",
#     help="Optional. Set the logging level",
# )
# @click.option(
#     "--log_to_tmp",
#     is_flag=True,
#     show_default=True,
#     default=False,
#     help=(
#         "Optional. Whether to log to system temp folder instead of console."
#         " This is useful for local debugging."
#     ),
# )
# @click.option(
#     "--trace_to_cloud",
#     is_flag=True,
#     show_default=True,
#     default=False,
#     help="Optional. Whether to enable cloud trace for telemetry.",
# )
# @click.argument(
#     "agents_dir",
#     type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
#     default=os.getcwd(),
# )
def web(
    agents_dir: str,
    log_to_tmp: bool = True,
    session_db_url: str = "",
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
    port: int = 8000,
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

    # from google.adk.cli.fast_api import get_fast_api_app
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
