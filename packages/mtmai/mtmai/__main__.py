import asyncio
import os

import typer
from dotenv import load_dotenv

import mtmai.core.bootstraps as bootstraps
from mtmai.core.config import settings

app = typer.Typer(invoke_without_command=True)


def setup_env():
    load_dotenv()
    bootstraps.bootstrap_core()

    if os.path.exists("../gomtm/env/dev.env"):
        load_dotenv(dotenv_path=os.path.join("../gomtm/env/dev.env"))
    MTM_DATABASE_URL = os.getenv("MTM_DATABASE_URL")
    if MTM_DATABASE_URL:
        os.environ["AUTOGENSTUDIO_DATABASE_URI"] = MTM_DATABASE_URL

    os.environ["AUTOGENSTUDIO_TEAM_FILE"] = "data.json"


setup_env()


@app.command()
def serve(
    team: str = "",
    host: str = "127.0.0.1",
    port: int = 8084,
    workers: int = 1,
    docs: bool = False,
):
    """
    Serve an API Endpoint based on an AutoGen Studio workflow json file.

    Args:
        team (str): Path to the team json file.
        host (str, optional): Host to run the UI on. Defaults to 127.0.0.1 (localhost).
        port (int, optional): Port to run the UI on. Defaults to 8084
        workers (int, optional): Number of workers to run the UI with. Defaults to 1.
        reload (bool, optional): Whether to reload the UI on code changes. Defaults to False.
        docs (bool, optional): Whether to generate API docs. Defaults to False.

    """

    # os.environ["AUTOGENSTUDIO_API_DOCS"] = str(docs)
    # os.environ["AUTOGENSTUDIO_TEAM_FILE"] = team

    # validate the team file
    # if not os.path.exists(team):
    #     raise ValueError(f"Team file not found: {team}")

    # uvicorn.run(
    #     "autogenstudio.web.serve:app",
    #     host=host,
    #     port=port,
    #     workers=workers,
    #     reload=False,
    # )

    from mtmai.core.logging import get_logger
    from mtmai.server import serve

    logger = get_logger()
    logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
    asyncio.run(serve())


# @app.command()
# def gradio():
#     from mtmai.gradio_app import demo

#     demo.launch(
#         share=True,
#         server_name="0.0.0.0",
#         server_port=18089,
#     )


@app.command()
def worker(
    url: str = typer.Option("http://127.0.0.1:8383", help="Worker server URL"),
):
    from mtmai.worker import WorkerApp

    worker_app = WorkerApp(url)
    asyncio.run(worker_app.deploy_mtmai_workers())


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # 如果没有指定子命令，默认执行 serve 命令
        ctx.invoke(serve)


def run():
    app()


if __name__ == "__main__":
    app()
