# 原文章： https://blog.csdn.net/ifhuke/article/details/127625901

# 原代码： https://github.com/accelerator1737/text_classify

# 文本多分类

Multiclassify text with pytorch

## 主要环境配置

- torch==1.8.1+cu101
- torchvision==0.9.1+cu101
- tqdm==4.64.0
- numpy==1.21.5

## 各文件的作用

- data_process_module.py
  数据预处理的文件
- main.py
  需要运行的文件
- RNNmodel.py
  所有的超参数设置以及RNN模型的定义
- trian_best_model.py
  训练的相关文件
