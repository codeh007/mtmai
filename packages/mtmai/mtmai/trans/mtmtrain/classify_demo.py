import pandas as pd
import requests
from bs4 import BeautifulSoup
from datasets import load_dataset
from fastapi import APIRouter
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    DefaultDataCollator,
    Trainer,
    TrainingArguments,
    pipeline,
)

router = APIRouter()


@router.get("/classify_demo2")
async def classifyDemo2():
    print("文本分类训练2开始")
    try:
        # 假设已有带标签的训练集
        training_data = [
            {
                "title": "Tech Article",
                "content": "This is a tech-related article.",
                "category": "Tech",
            },
            {
                "title": "Sports News",
                "content": "Latest sports news.",
                "category": "Sports",
            },
            {
                "title": "General Article",
                "content": "A general article on various topics.",
                "category": "Other",
            },
            # ...
        ]

        # 转为DataFrame
        df_train = pd.DataFrame(training_data)

        # 划分训练集和测试集
        df_train, df_test = train_test_split(df_train, test_size=0.2, random_state=42)

        # 使用transformers的pipeline进行分类
        classifier = pipeline(
            "text-classification",
            model="bert-base-uncased",
            tokenizer="bert-base-uncased",
        )
        classifier.train(df_train, max_epochs=3)

        # 在测试集上进行预测
        predictions = classifier.predict(df_test["content"])

        # 评估分类器性能
        accuracy = accuracy_score(df_test["category"], predictions)
        print(f"Accuracy: {accuracy}")

        # 使用训练好的模型进行新文章分类
        new_article = {
            "title": "New Article",
            "content": "This is a new article on technology.",
            "category": None,
        }
        predicted_category = classifier.predict([new_article["content"]])[0]

        print(f"Predicted Category: {predicted_category}")

        print("文本分类训练结束（只是一个例子，内部没有正式启动训练的过程）")
        return {"message": "success"}
    except Exception as e:
        print(f"classifyDemo2 出错 {e}")
        return {"message": "error"}


@router.get("/classify_demo3")
async def classifyDemo3():
    try:
        # 参考文章： https://developer.aliyun.com/article/1111665
        # RSS feed link and their categories. Will iterate them one by one.
        # Have mentioned only one feed for demo purposes
        timesofindia = {
            "world": "http://timesofindia.indiatimes.com/rssfeeds/296589292.cms"
        }
        for category, rsslink in timesofindia.items():
            print(f"Processing for category: {category}. \nRSS link: {rsslink}")
            # get the webpage URL and read the html
            rssdata = requests.get(rsslink)
            # print(rssdata.content)
            soup = BeautifulSoup(rssdata.content)
            print(soup.prettify())

        # get all news items. It has title, description, link, guid, pubdate for each news items.
        # Lets call this items and we will iterate thru it
        allitems = soup.find_all("item")  # print one news item/healine to check
        for item in range(len(allitems)):
            print("Processing news-item #:", item)
            title = allitems[item].title.text
            link = allitems[item].guid.text
            pubdate = allitems[item].pubdate.text
            print("TITLE:", title)
            print("LINK:", link)
            print("PUBDATE:", pubdate)

        # 提取文章
        # Function to fetch each news link to get news essay
        def fetch_news_text(link):
            # read the html webpage and parse it
            soup = BeautifulSoup(requests.get(link).content, "html.parser")
            # fetch the news article text box
            # these are with element <div class="_3WlLe clearfix">
            text_box = soup.find_all("div", attrs={"class": "_3WlLe clearfix"})
            # extract text and combine
            news_text = str(". ".join(t.text.strip() for t in text_box))
            return news_text  # using the above function, process text

        news_articles = [
            {
                "Feed": "timesofindia",
                "Category": category,
                "Headline": allitems[item].title.text,
                "Link": allitems[item].guid.text,
                "Pubdate": allitems[item].pubdate.text,
                "NewsText": fetch_news_text(allitems[item].guid.text),
            }
            for item in range(len(allitems))
        ]
        news_articles = pd.DataFrame(news_articles)
        news_articles.head(3)

        # 为了进行文本清理，我使用了文本的预处理，这些步骤是删除HTML标记，特殊字符，数字，标点符号，停用词，处理重音字符，扩展收缩，词干和词形等。
        # 在这里，我将这些预处理步骤放到一个函数中，该函数将返回干净且标准化的语料库。
        # test normalize cleanup on one article
        # clean_sentences = normalize_corpus([news_articles['NewsText'][0]])
        clean_sentences = normalize_corpus(news_articles["NewsText"])
        print("clean_sentences", clean_sentences)
        return {"message": "success"}
    except Exception as e:
        print(f"classifyDemo3 出错 {e}")
        return {"message": "error"}


@router.get("/classify_demo4")
async def classifyDemo4():
    """
    本地训练，训练完成后自动将模型上传到 huggingface
    "# 来自官方例子： https://huggingface.co/docs/transformers/v4.37.2/en/tasks/question_answering\n",
    "# 简单的问答系统，使用官方数据集训练，训练完成后发布到自己的 huggingface仓库。"
    """
    print("classify_demo4 开始")
    try:
        # 登录
        print("登录到hugging face")
        # hf.notebook_login()
        squad = load_dataset("squad", split="train[:5000]")
        squad = squad.train_test_split(test_size=0.2)
        squad["train"][0]

        # 步骤2：
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

        def preprocess_function(examples):
            questions = [q.strip() for q in examples["question"]]
            inputs = tokenizer(
                questions,
                examples["context"],
                max_length=384,
                truncation="only_second",
                return_offsets_mapping=True,
                padding="max_length",
            )

            offset_mapping = inputs.pop("offset_mapping")
            answers = examples["answers"]
            start_positions = []
            end_positions = []

            for i, offset in enumerate(offset_mapping):
                answer = answers[i]
                start_char = answer["answer_start"][0]
                end_char = answer["answer_start"][0] + len(answer["text"][0])
                sequence_ids = inputs.sequence_ids(i)

                # Find the start and end of the context
                idx = 0
                while sequence_ids[idx] != 1:
                    idx += 1
                context_start = idx
                while sequence_ids[idx] == 1:
                    idx += 1
                context_end = idx - 1

                # If the answer is not fully inside the context, label it (0, 0)
                if (
                    offset[context_start][0] > end_char
                    or offset[context_end][1] < start_char
                ):
                    start_positions.append(0)
                    end_positions.append(0)
                else:
                    # Otherwise it's the start and end token positions
                    idx = context_start
                    while idx <= context_end and offset[idx][0] <= start_char:
                        idx += 1
                    start_positions.append(idx - 1)

                    idx = context_end
                    while idx >= context_start and offset[idx][1] >= end_char:
                        idx -= 1
                    end_positions.append(idx + 1)

            inputs["start_positions"] = start_positions
            inputs["end_positions"] = end_positions
            return inputs

        tokenized_squad = squad.map(
            preprocess_function,
            batched=True,
            remove_columns=squad["train"].column_names,
        )
        data_collator = DefaultDataCollator()
        print("数据准备就绪，开始训练")
        # from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
        model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased")
        training_args = TrainingArguments(
            output_dir="my_awesome_qa_model",
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            push_to_hub=True,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_squad["train"],
            eval_dataset=tokenized_squad["test"],
            tokenizer=tokenizer,
            data_collator=data_collator,
        )

        trainer.train()
        # 发布模型
        trainer.push_to_hub()
        return {"message": "success"}
    except Exception as e:
        print(f"classifyDemo4 出错 {e}")
        return {"message": str(e)}
