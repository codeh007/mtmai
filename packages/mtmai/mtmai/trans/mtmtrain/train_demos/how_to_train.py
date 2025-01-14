# 如何训练模型, 参考: https://github.com/huggingface/blog/blob/main/notebooks/01_how_to_train.ipynb

from pathlib import Path

from tokenizers import ByteLevelBPETokenizer

paths = [str(x) for x in Path().glob("**/*.txt")]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(
    files=paths,
    vocab_size=52_000,
    min_frequency=2,
    special_tokens=[
        "",
        "",
        "",
        "",
    ],
)


def train():
    tokenizer.save_model("EsperBERTo")
