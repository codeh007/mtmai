from bs4 import BeautifulSoup


def extract_title_from_html(html_content: str) -> str:
    """
    从html 中提取title
    """
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 查找title标签
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.text.strip()

    # 如果没有title标签，查找h1标签
    h1_tag = soup.find("h1")
    if h1_tag:
        return h1_tag.text.strip()

    # 如果没有h1标签，查找h2标签
    h2_tag = soup.find("h2")
    if h2_tag:
        return h2_tag.text.strip()

    # 如果都没有找到，返回空字符串
    return ""
