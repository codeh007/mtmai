"""
Acquire examples of click-bait and non-click-bait text
We will use the clickbait dataset for this example, which contains text that are both click-bait,
and not click-bait [1]. First, download those datasets. We will use wget to download them, but any tool will do.
参考: https://tembo.io/docs/product/stacks/ai/machine-learning
"""

# prep.py
import csv
import logging

# import threading
from pathlib import Path

from fastapi import APIRouter

from mtmai.core.config import settings
from mtmai.mtlibs.mtutils import download_and_extract_gz

router = APIRouter()
logger = logging.getLogger()


def start_trans_clickbait():
    logger.info("加载 clickbait 基础数据集")

    clickbait_data = f"{settings.storage_dir}/dataset/clickbait_data"
    non_clickbait_data = f"{settings.storage_dir}/dataset/non_clickbait_data"
    download_and_extract_gz(
        "https://github.com/bhargaviparanjape/clickbait/raw/master/dataset/clickbait_data.gz",
        clickbait_data,
    )
    download_and_extract_gz(
        "https://github.com/bhargaviparanjape/clickbait/raw/master/dataset/non_clickbait_data.gz",
        non_clickbait_data,
    )

    logger.info("合并 clickbait 训练数据")
    clickbait_data = [("text", "is_clickbait")]

    files = [clickbait_data, non_clickbait_data]
    for f in files:
        with Path.open(f) as file:
            is_clickbait = 1 if f == "clickbait_data" else 0
            for line in file:
                # Skip empty lines
                if line.strip():
                    clickbait_data.append((line.strip(), is_clickbait))

    training_data = Path(settings.storage_dir).joinpath("training_data.csv")
    with Path.open(training_data, mode="w", newline="") as file:
        writer = csv.writer(file)
        for item in clickbait_data:
            writer.writerow(item)

    logger.info("导入到数据库 TODO")
