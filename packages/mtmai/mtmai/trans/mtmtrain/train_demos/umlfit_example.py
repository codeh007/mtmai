# 使用 tweets 航空公司 数据集，用 ULMFit 模型，训练情感分析模型
# 文章: https://cloud.tencent.com/developer/article/1692358

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastai.text import TextLMDataBunch
from fastai.text.all import (
    AWD_LSTM,
    language_model_learner,
)

# from fastai.text import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from tensorflow.keras import Sequential

from mtmtrain import dataset
from mtmtrain.utils import clean_ascii

# Setting Seed
np.random.seed(42)

# Main data file
# DATA_DIR = "sample_data/Tweets.csv"

logger = logging.getLogger()


def train():
    all_datasets = ["common/Tweets.csv"]
    logger.info("加载数据集 %s", all_datasets)
    for ds in all_datasets:
        dataset.load_dataset(ds)
    df = pd.read_csv(dataset.get_dataset_path("common/Tweets.csv"))

    # LabelEncoder to change positive, negative and neutral to numbers (classes)
    labelEncoder = LabelEncoder()

    def gather_texts_and_labels(df=None, test_size=0.15, random_state=42):
        """
        Gathers the text and the corresponding labels from the dataset and splits it.

        Arguments:
            df: Pandas DataFrame
            test_size: represents the test size
            random_state: represents the random state

        Returns
        -------
            (x_train, x_test, y_train, y_test, new_df)
        """
        # texts
        texts = df["text"].values

        # encoding labels (positive, neutral, negative)
        df["airline_sentiment"] = labelEncoder.fit_transform(df["airline_sentiment"])
        labels = df["airline_sentiment"].values

        # changing the order for fastai tokenizers to capture data.
        new_df = pd.DataFrame(data={"label": labels, "text": texts})

        df_train, df_test = train_test_split(
            new_df,
            stratify=new_df["label"],
            test_size=test_size,
            random_state=random_state,
        )
        df_train, df_val = train_test_split(
            df_train,
            stratify=df_train["label"],
            test_size=test_size,
            random_state=random_state,
        )

        print(f"Training: {len(df_train)}, Testing: {len(df_test)}, Val: {len(df_val)}")

        return df_train, df_test, df_val, new_df

    def describe_dataset(df=None):
        """
        Describes the dataset

        Arguments:
            df: Pandas Dataframe
        """
        print(df["airline_sentiment"].value_counts())
        print(df["airline"].value_counts())
        print(
            f"\nMean airline_sentiment_confidence is {df.airline_sentiment_confidence.mean()}"
        )

    # Optional
    def add_negativereason_to_text(df=None):
        # change negativereason to "" if NaN else remain as is.
        df["negativereason"] = df["negativereason"].apply(
            lambda x: "" if pd.isna(x) else x
        )

        # add negativereason to text
        df["text"] = df["text"] + df["negativereason"]

    add_negativereason_to_text(df)
    df["text"] = df["text"].apply(clean_ascii)

    describe_dataset(df)
    df_train, df_test, df_val, new_df = gather_texts_and_labels(df)

    mapping = dict(
        list(
            zip(
                labelEncoder.transform(labelEncoder.classes_),
                labelEncoder.classes_,
                strict=False,
            )
        )
    )
    print(f"Mapping is {mapping}")

    logger.info("显示数据柱状图表")
    df["airline"].value_counts().plot.bar()
    plt.show()
    df["airline_sentiment"].value_counts().plot.bar()
    plt.show()
    data = pd.crosstab(df["airline"], df["airline_sentiment"])
    print(data)

    print("""
          Before any machine learning experiment, we should always set up a baseline and compare our results with the it.
To setup the baseline, we will use a word2vec embedding matrix to try to predict sentiment.
To Load our word2vec, we will be using embedding layer, followed by basic Feed Forward NN to predict sentiment.
We could have also loaded a pretrained word2vec or glove embeddings to be fed into our embedding layer.
We could have used a LSTM or CNN after the embedding layer followed by a softmax activation.
""")

    # The word2vec requires sentences as list of lists.
    texts = df["text"].apply(clean_ascii).values
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=5000, oov_token="<OOV>")

    # fitting
    tokenizer.fit_on_texts(texts)

    vocab_size = len(tokenizer.word_index) + 1

    # max length to be padded (batch_size, 100)
    max_length = 100

    train_text = tokenizer.texts_to_sequences(df_train["text"].values)
    test_text = tokenizer.texts_to_sequences(df_test["text"].values)

    # getting the padded length of 100
    padded_train_text = keras.preprocessing.sequence.pad_sequences(
        train_text, max_length, padding="post"
    )
    padded_test_text = keras.preprocessing.sequence.pad_sequences(
        test_text, max_length, padding="post"
    )

    labels_train = keras.utils.to_categorical(df_train["label"].values, 3)
    labels_test = keras.utils.to_categorical(df_test["label"].values, 3)

    metrics = [keras.metrics.Accuracy()]

    # (创建了一个简单的文本分类模型，使用嵌入层对词汇进行嵌入, 并通过全连接层进行分类)
    # 创建一个顺序模型。
    net = Sequential()
    # 添加嵌入层，将词汇表大小 vocab_size 映射到 50 维的嵌入空间。输入长度为 100。
    net.add(keras.layers.Embedding(vocab_size, 50, input_length=max_length))
    # 将嵌入层的输出展平, 以便传递到全连接层。
    net.add(keras.layers.Flatten())
    # 添加一个具有 512 个神经元的全连接层，激活函数为 ReLU。
    net.add(keras.layers.Dense(512, activation="relu"))
    # 添加一个具有 3 个神经元的全连接层, 激活函数为 softmax, 用于分类。
    net.add(keras.layers.Dense(3, activation="softmax"))

    # 编译模型, 使用 Adam 优化器。 使用类别交叉熵损失函数, 使用定义的度量来评估模型的性能。
    net.compile(
        optimizer="adam", loss=keras.losses.categorical_crossentropy, metrics=metrics
    )
    logger.info("显示模型摘要")
    net.summary()

    # 开始训练模型
    net.fit(padded_train_text, labels_train, epochs=10, validation_split=0.2)

    def test_baseline_sentiment(text):
        """
        Test the baseline model

        Arguments:
        text:str
        """
        padded_text = keras.preprocessing.sequence.pad_sequences(
            tokenizer.texts_to_sequences([text]), max_length, padding="post"
        )
        print(net.predict(padded_text).argmax(axis=1))

    net.evaluate(padded_test_text, labels_test)
    preds = net.predict(padded_test_text).argmax(axis=1)

    logger.info("Loading the Language Model and Fine Tuning")

    data_lm = TextLMDataBunch.from_df(train_df=df_train, valid_df=df_val, path="")

    # Saving the data_lm as backup
    data_lm.save("data_lm_twitter.pkl")  # saving as a back stop

    # Loading the language model (AWD_LSTM)
    learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)

    print(learn)
