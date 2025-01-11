"""
# 模型训练, 让llama3.18b模型具备将现代汉语转换为古文风格的文章
- 资料库: https://github.com/NiuTrans/Classical-Modern
- 参考别人的训练数据集： https://huggingface.co/datasets/AISPIN/shiji-70liezhuan
- 别人训练好的模型 参考： https://huggingface.co/AISPIN/Llama-3.1-8B-bnb-4bit-wenyanwen
- 参考视频： https://www.youtube.com/watch?v=Tq6qPw8EUVg

"""

import logging
import os

from fastapi import APIRouter

from mtmlib.queue.queue import Message

# from mtmai.core.queue import Message

router = APIRouter()
logger = logging.getLogger()


def tran_guwen_consumer(msg: Message):
    import pandas as pd

    logger.info("start_tran_guwen")
    folder_path = r"双语数据/史记/七十列传"

    # get all subfolders in the folder, then for each subfolder, get source file and target file,
    # then read the content of the files then combine them into a dateset, the source file is the input field,
    # the target file is the output field, and the target file is the output field

    def get_files(folder_path):
        subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
        print(subfolders)
        dataset = []

        source_file = "source.txt"
        target_file = "target.txt"
        for x in subfolders:
            with open(os.path.join(x, source_file), encoding="utf-8") as f:
                source_content = f.read()
            with open(os.path.join(x, target_file), encoding="utf-8") as f:
                target_content = f.read()

            # source and target needs to be split by "\n"
            source_content = source_content.split("\n")
            target_content = target_content.split("\n")

            # source and target should be saved into dateset line by line
            for i in range(len(source_content)):
                dataset.append([source_content[i], target_content[i]])

        return dataset

    dataset = get_files(folder_path)

    # add one column "instruction" with the content "请把古文翻译成现代汉语" to the dataset
    df = pd.DataFrame(dataset, columns=["source", "target"])
    df["instruction"] = "请把现代汉语翻译成古文"

    # rename the columns: source -> output, target -> input
    df.rename(columns={"source": "output", "target": "input"}, inplace=True)

    # print length of the dataset
    print(len(df))

    # save the dataset into a jsonl file
    df.to_json("dataset.jsonl", orient="records", lines=True, force_ascii=False)
