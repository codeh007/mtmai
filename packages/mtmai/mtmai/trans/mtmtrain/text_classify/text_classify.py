import torch

# from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import pipeline


def tran():
    # 定义分类函数
    def classify_text(input_text, candidate_labels):
        # test_input=""I have a problem with my iphone that needs to be resolved asap!!","
        classifyResult = pipeModel1(
            input_text,
            candidate_labels=candidate_labels,
        )
        # 挑选最匹配的一个
        max_score_index = classifyResult["scores"].index(max(classifyResult["scores"]))
        max_label = classifyResult["labels"][max_score_index]
        # ret = classifyResult[0]
        return max_label

    # version = pkg_resources.get_distribution("mtmtrain").version
    # print("版本号2222： ", version)

    # version = version("mtmtrain")
    # print("版本号：：", version)

    # 固定随机数，可以确保相同环境下运算的结果相同。
    seed_value = 42
    torch.manual_seed(seed_value)

    # 使用 GPU 如果可用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 加载预训练的 DistilBERT 分类模型
    model_name = "distilbert-base-uncased"

    # 假设 category_labels 是你的类别标签列表，例如 ["News", "Technology", "Food"]
    # category_labels = ["News", "Technology", "Food"]
    # num_labels = len(category_labels)

    # tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    # model = DistilBertForSequenceClassification.from_pretrained(model_name, problem_type="multi_label_classification")

    # model.to(device)

    pipeModel1 = pipeline(model="facebook/bart-large-mnli")
