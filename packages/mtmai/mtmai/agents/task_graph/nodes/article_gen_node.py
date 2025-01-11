from langchain_core.runnables import RunnableConfig

from mtmai.agents.task_graph.task_state import ArticleArtifact, TaskState
from mtmai.core.logging import get_logger

logger = get_logger()


class ArticleGenNode:
    def __init__(self):
        pass

    async def __call__(self, state: TaskState, config: RunnableConfig):
        logger.info("进入 article_gen_node")
        messages = state.messages
        user_input = state.user_input

        article_artifact = ArticleArtifact(
            id="1",
            content="example1",
            title="",
            type="text",
            language="markdown",
        )
        return {
            "human_ouput_message": "已经生成了一篇文章",
            "artifacts": [article_artifact.model_dump()],
        }
