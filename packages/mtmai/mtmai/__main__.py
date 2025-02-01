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
# def main():
#     @click.group(invoke_without_command=True)
#     @click.pass_context
#     def cli(ctx):
#         if ctx.invoked_subcommand is None:
#             # 如果没有指定子命令，默认执行 serve 命令
#             ctx.invoke(serve)

#     @cli.command()
#     def serve():
#         from mtmai.core.config import settings
#         from mtmai.core.logging import get_logger
#         from mtmai.server import serve

#         logger = get_logger()
#         logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
#         asyncio.run(serve())

#     cli()

# @app.command()
# def ui(
#     host: str = "127.0.0.1",
#     port: int = 8082,
#     workers: int = 1,
#     reload: Annotated[bool, typer.Option("--reload")] = False,
#     docs: bool = True,
#     appdir: str = None,
#     database_uri: Optional[str] = None,
#     upgrade_database: bool = False,
# ):
#     """
#     Run the AutoGen Studio UI.

#     Args:
#         host (str, optional): Host to run the UI on. Defaults to 127.0.0.1 (localhost).
#         port (int, optional): Port to run the UI on. Defaults to 8081.
#         workers (int, optional): Number of workers to run the UI with. Defaults to 1.
#         reload (bool, optional): Whether to reload the UI on code changes. Defaults to False.
#         docs (bool, optional): Whether to generate API docs. Defaults to False.
#         appdir (str, optional): Path to the AutoGen Studio app directory. Defaults to None.
#         database-uri (str, optional): Database URI to connect to. Defaults to None.
#     """
#     setup_env()

#     os.environ["AUTOGENSTUDIO_API_DOCS"] = str(docs)
#     if appdir:
#         os.environ["AUTOGENSTUDIO_APPDIR"] = appdir
#     if database_uri:
#         os.environ["AUTOGENSTUDIO_DATABASE_URI"] = database_uri
#     if upgrade_database:
#         os.environ["AUTOGENSTUDIO_UPGRADE_DATABASE"] = "1"

#     uvicorn.run(
#         "autogenstudio.web.app:app",
#         host=host,
#         port=settings.PORT,
#         workers=workers,
#         reload=reload,
#         reload_excludes=["**/alembic/*", "**/alembic.ini", "**/versions/*"]
#         if reload
#         else None,
#     )


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


@app.command()
def gradio():
    from mtmai.gradio_app import demo

    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=18089,
    )


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # 如果没有指定子命令，默认执行 serve 命令
        ctx.invoke(serve)


def run():
    app()


if __name__ == "__main__":
    app()
