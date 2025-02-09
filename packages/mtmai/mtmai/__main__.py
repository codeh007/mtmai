import asyncio

import typer

import mtmai.core.bootstraps as bootstraps
from mtmai.core.config import settings

bootstraps.bootstrap_core()
app = typer.Typer(invoke_without_command=True)


@app.command()
def serve(
    team: str = "",
    host: str = "127.0.0.1",
    port: int = 8084,
    workers: int = 1,
    docs: bool = False,
):
    from mtmai.core.logging import get_logger
    from mtmai.server import serve

    logger = get_logger()
    logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
    asyncio.run(serve())


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # 如果没有指定子命令，默认执行 serve 命令
        ctx.invoke(serve)

def run():
    app()

if __name__ == "__main__":
    app()
