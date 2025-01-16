

def zhparser_cut(input: str):
    import jieba  # 这个库加载时间比较长
    return jieba.cut(input)
