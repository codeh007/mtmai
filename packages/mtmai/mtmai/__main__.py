import asyncio

import typer

import mtmai.core.bootstraps as bootstraps
from mtmai.agents.worker_agent.worker_agent import WorkerAgent

bootstraps.bootstrap_core()
app = typer.Typer(invoke_without_command=True)


@app.callback()
def main(ctx: typer.Context):
    # 如果没有指定子命令，默认执行 serve 命令
    if ctx.invoked_subcommand is None:
        ctx.invoke(run)


@app.command()
def run():
    asyncio.run(WorkerAgent().run(task="Hello, world!"))


@app.command()
def host():
    import grpc_host as grpc_host

    asyncio.run(grpc_host.run_ag_grpc_host())


if __name__ == "__main__":
    app()
