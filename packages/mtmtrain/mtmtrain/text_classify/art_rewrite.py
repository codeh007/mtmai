import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import pipeline

# 固定随机数，可以确保相同环境下运算的结果相同。
seed_value = 42
torch.manual_seed(seed_value)

# 使用 GPU 如果可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练的 DistilBERT 分类模型
model_name = "distilbert-base-uncased"

pipeModel1 = pipeline(model="facebook/bart-large-mnli")

# 给定文章，改写文章，输出的结果将是最终文章。
def art_rewrite(title, content, candidate_labels):
    # test_input=""I have a problem with my iphone that needs to be resolved asap!!","
    classifyResult=pipeModel1(input_text, candidate_labels=candidate_labels,)
    # 挑选最匹配的一个
    max_score_index = classifyResult["scores"].index(max(classifyResult["scores"]))
    max_label = classifyResult["labels"][max_score_index]
    return max_label
