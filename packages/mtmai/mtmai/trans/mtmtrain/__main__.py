import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from mtmtrain.core.config import settings

sys.path.insert(0, str(Path("mtmlib").resolve()))
from mtmlib.logging import LoggingOptions, setup_logging

load_dotenv()

setup_logging(option=LoggingOptions())
logger = logging.getLogger("mtmtrain")


"""
    在coleb 的使用方式:
    !pip install -U --no-cache-dir "mtmtrain" --index-url https://pypi.org/simple \
    && mtmtrain init
"""


def task_a(alpha):
    print("task a", alpha)


def task_b(beta, gamma):
    print("task b", beta, gamma)


def worker():
    if not settings.MTMAI_API_BASE:
        print("require server url")
        return
    from mtmtrain.worker import worker_start

    worker_start()


def down_dataset():
    if not settings.MTMAI_API_BASE:
        print("require server url")
        return
    from mtmai_client.api.dataset import dataset_dataset_download
    from mtmai_client.client import Client

    client = Client(base_url=settings.MTMAI_API_BASE)

    local_dataset_dir = ".vol/datasets"
    all_datasets = ["text_classify/bbc-text.csv"]
    for ds in all_datasets:
        response = dataset_dataset_download.sync(client=client, dataset_path=ds)
        dataset_path = Path(local_dataset_dir).joinpath(ds)
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        dataset_path.write_text(response)
        logger.info("数据集下载完成 %s", dataset_path.resolve())


def main():
    print("[🚀 mtmtrain]")

    parser = argparse.ArgumentParser(description="mtmtrain")

    # 添加全局参数
    parser.add_argument(
        "-s",
        "--server-url",
        help="Specify the backend server URL.",
        default="http://localhost:8444",  # 默认 URL
        type=str,
    )
    subparsers = parser.add_subparsers(dest="subparser")
    parser_a = subparsers.add_parser("task_a")
    parser_a.add_argument("-a", "--alpha", dest="alpha", help="Alpha description")

    parser_b = subparsers.add_parser("task_b")
    parser_b.add_argument("-b", "--beta", dest="beta", help="Beta description")
    parser_b.add_argument(
        "-g", "--gamma", dest="gamma", default=42, help="Gamma description"
    )

    parser_worker = subparsers.add_parser("worker")

    parser_down_dataset = subparsers.add_parser("down_dataset")

    args = parser.parse_args()
    # 设置全局的后端 URL
    settings.MTMAI_API_BASE = args.server_url

    # 调用相应的子命令
    if args.subparser == "task_a":
        task_a(args.alpha)
    elif args.subparser == "task_b":
        task_b(args.beta, args.gamma)
    elif args.subparser == "worker":
        worker()
    elif args.subparser == "down_dataset":
        down_dataset()
    else:
        parser.print_help()

    # kwargs = vars(parser.parse_args())
    # globals()[kwargs.pop("subparser")](**kwargs)

    # # 创建子命令解析器
    # subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    # # 定义 'init' 子命令
    # subparsers.add_parser("init", help="Run initialization.")

    # # 定义 'worker' 子命令
    # subparsers.add_parser("worker", help="Start the worker process.")

    # # 定义 'show1' 子命令
    # subparsers.add_parser("show1", help="Show visual output.")
    # subparsers.add_parser("down_dataset", help="Show visual output.")

    # # 定义 'text_classify' 子命令
    # subparsers.add_parser("text_classify", help="Run text classification training.")

    # args = parser.parse_args()

    # if args.command == "init":
    #     from mtmtrain import env

    #     print("Initializing environment...")
    #     env.init_env()
    #     print("Environment initialized.")
    # elif args.command == "worker":
    #     from mtmtrain.worker import worker_start

    #     settings.MTMAI_API_BASE = args.server_url
    #     worker_start()

    # elif args.command == "show1":
    #     from IPython.display import HTML, display

    #     def show_visual_output():
    #         display(HTML("<h1>Processed Data:</h1><pre>88888</pre>"))

    #     show_visual_output()

    # elif args.command == "text_classify":
    #     from mtmtrain import text_classify

    #     text_classify.train()

    # elif args.command == "down_dataset":
    #     from mtmai_client.client import Client

    #     client = Client()
    #     from mtmai_client.api.dataset import dataset_dataset_download

    #     dataset_dataset_download.sync(
    #         client=client, dataset_path="text_classify/bbc-text.csv"
    #     )

    # else:
    #     print("Unknown command", args.command)


if __name__ == "__main__":
    main()
