import asyncio

import click
from dotenv import load_dotenv

load_dotenv()

import mtmai.core.bootstraps as bootstraps

bootstraps.bootstrap_core()


def main():
    # @click.group()
    # def cli():
    #     pass

    @click.group(invoke_without_command=True)
    @click.pass_context
    def cli(ctx):
        if ctx.invoked_subcommand is None:
            # 如果没有指定子命令，默认执行 serve 命令
            ctx.invoke(serve)

    @cli.command()
    def serve():
        from mtmai.core.config import settings
        from mtmai.core.logging import get_logger
        from mtmai.server import serve

        logger = get_logger()
        logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
        asyncio.run(serve())

    # @cli.command()
    # @click.option("--url", required=False)
    # def worker(url):
    #     from mtmai.worker import WorkerApp

    #     worker_app = WorkerApp(url)
    #     asyncio.run(worker_app.deploy_mtmai_workers())

    @cli.command()
    def gradio():
        from mtmai.gradio_app import demo

        demo.launch(
            share=True,
            server_name="0.0.0.0",
            server_port=18089,
        )

    cli()


if __name__ == "__main__":
    main()
