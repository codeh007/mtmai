import asyncio

import typer

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
    from worker_app import run_worker

    asyncio.run(run_worker())


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


if __name__ == "__main__":
    app()
