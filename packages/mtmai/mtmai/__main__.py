import asyncio

import click
from dotenv import load_dotenv

load_dotenv()


def main():

    @click.group()
    def cli():
        pass

    # @cli.command()
    # def serve():
    #     from mtmai.core.config import settings
    #     from mtmai.core.logging import get_logger
    #     from mtmai.server import serve


    #     logger = get_logger()
    #     logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
    #     asyncio.run(serve())

    @cli.command()
    @click.option("--url", required=False)
    def worker(url):
        from mtmai.worker import WorkerApp

        worker_app = WorkerApp(url)
        asyncio.run(worker_app.deploy_mtmai_workers(url))

    @cli.command()
    @click.option("--url", required=False)
    def worker2(url):
        from mtmai.worker import WorkerApp

        worker_app = WorkerApp(url)
        asyncio.run(worker_app.deploy_mtmai_workers(url))

    cli()


if __name__ == "__main__":
    main()
