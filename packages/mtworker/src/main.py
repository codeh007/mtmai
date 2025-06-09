import typer
from loguru import logger
from mtmai.core import bootstrap_core

bootstrap_core()
app = typer.Typer(invoke_without_command=True)


@app.callback()
def main(ctx: typer.Context):
  # 默认执行 serve 命令
  if ctx.invoked_subcommand is None:
    ctx.invoke(run)


@app.command()
def run():
  logger.info("mtworker starting ...")


if __name__ == "__main__":
  app()
