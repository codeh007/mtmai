import logging

import numpy as np
import pandas as pd
import transformers
from sklearn.model_selection import train_test_split

from mtmtrain import dataset
from mtmtrain.ipy import ipyutils

logger = logging.getLogger()


def train():
    all_datasets = ["text_classify/bbc-text.csv"]

    logger.info("加载数据集 %s", all_datasets)
    for ds in all_datasets:
        dataset.load_dataset(ds)
    # Download the dataset and put it in subfolder called data
    datapath = dataset.get_dataset_path("text_classify/bbc-text.csv")
    df = pd.read_csv(datapath)
    df = df[["category", "text"]]

    logging.info("简单信息浏览")
    ipyutils.display(df.head())

    # Renaming, Input -> X, Output -> y
    X = df["text"]
    y = np.unique(df["category"], return_inverse=True)[1]
    logger.info("category 列 %s", y)
    print(y)

    logging.info("开始用 TensorFlow  Building a Text Classification")

    tokenizer = transformers.DistilBertTokenizer.from_pretrained(
        "distilbert-base-uncased"
    )
    X_tf = [
        tokenizer(text, padding="max_length", max_length=512, truncation=True)[
            "input_ids"
        ]
        for text in X
    ]
    X_tf = np.array(X_tf, dtype="int32")

    # Train/test split

    X_tf_train, X_tf_test, y_tf_train, y_tf_test = train_test_split(
        X_tf, y, test_size=0.3, random_state=42, stratify=y
    )
    print("Shape of training data: ", X_tf_train.shape)
    print("Shape of test data: ", X_tf_test.shape)

    logging.info("Build the Model")
    # Get BERT layer
    config = transformers.DistilBertConfig(dropout=0.2, attention_dropout=0.2)
    dbert_tf = transformers.TFDistilBertModel.from_pretrained(
        "distilbert-base-uncased", config=config, trainable=False
    )
    logger.info(dbert_tf)

    # Let's create a sample of size 5 from the training data
    sample = X_tf_train[0:5]
    print("Object type: ", type(dbert_tf(sample)))
    print("Output format (shape): ", dbert_tf(sample)[0].shape)
    print(
        "Output used as input for the classifier (shape): ",
        dbert_tf(sample)[0][:, 0, :].shape,
    )
