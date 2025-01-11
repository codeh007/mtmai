import logging
from pathlib import Path

from mtmai_client.client import Client

from mtmtrain.core.config import settings

logger = logging.getLogger()

local_dataset_dir = "datasets"


def download_dataset(dataset: str):
    from mtmai_client.api.dataset import dataset_dataset_download

    client = Client(base_url=settings.MTMAI_API_BASE)

    # for ds in all_datasets:
    response = dataset_dataset_download.sync(client=client, dataset_path=dataset)
    dataset_path = get_dataset_path(dataset)
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    dataset_path.write_text(response)
    logger.info("数据集下载完成 %s", dataset_path.resolve())


def down_dataset_from_url(url: str):
    localbase_dir = Path(settings.storage_dir).joinpath(local_dataset_dir)
    # 输入的网址形如： https://cdn-datasets.huggingface.co/EsperBERTo/data/oscar.eo.txt

    # 使用 httpx 下载文件，并且将文件保存到 f{localbase_dir}/oscar.eo.txt 下。


def load_dataset(dataset_name: str):
    local_path = (
        Path(settings.storage_dir).joinpath(local_dataset_dir).joinpath(dataset_name)
    )
    if not local_path.exists():
        download_dataset(dataset_name)


def get_dataset_path(dataset: str):
    # settings.storage_dir 值为 ".vol", local_dataset_dir= "datasets"
    # settings.storage_dir 值为 ".vol", local_dataset_dir= "datasets", ="common/Tweets.csv"
    a = Path(settings.storage_dir).joinpath(local_dataset_dir).joinpath(dataset)
    print(str(a))
    return a
