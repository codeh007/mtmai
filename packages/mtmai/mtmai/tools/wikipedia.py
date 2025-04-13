import logging

logger = logging.getLogger()


def format_doc(doc, max_length=1000):
    related = "- ".join(doc.metadata["categories"])
    return f"### {doc.metadata['title']}\n\nSummary: {doc.page_content}\n\nRelated\n{related}"[
        :max_length
    ]


def format_docs(docs):
    return "\n\n".join(format_doc(doc) for doc in docs)


class MtmTopicDocRetriever:
    """根据给定的主题列表，从网络获取相关主题的文章"""

    def __init__(self):
        pass

    async def retrive(self, topics: list[str], max_retry=3, min_docs_required=1):
        logger.info(
            f"MtmTopicDocRetriever 开始检索相关文档:{min_docs_required}, {topics}"
        )
        from langchain_community.retrievers import WikipediaRetriever

        wikipedia_retriever = WikipediaRetriever(
            load_all_available_meta=True, top_k_results=1
        )
        all_docs = []
        retry_count = 0

        while retry_count < max_retry and len(all_docs) < min_docs_required:
            retrieved_docs = await wikipedia_retriever.abatch(
                topics, return_exceptions=True
            )

            for docs in retrieved_docs:
                if isinstance(docs, BaseException):
                    logger.error(f"wikipedia 检索失败: {docs}")
                    continue
                if len(docs) == 0:
                    logger.error(f"wikipedia 检索失败,0 文档: {docs}")
                    continue
                all_docs.extend(docs)

            if len(all_docs) < min_docs_required:
                logger.warning(
                    f"重试获取文档，当前重试次数: {retry_count + 1}，已获取 {len(all_docs)} 个文档，目标数量: {min_docs_required}"
                )
                retry_count += 1

        if len(all_docs) < min_docs_required:
            logger.error(
                f"在{max_retry}次重试后仍未获取到足够的文档。目标数量: {min_docs_required}，实际获取: {len(all_docs)}"
            )
            if len(all_docs) == 0:
                return None

        formatted = format_docs(all_docs)

        return formatted
