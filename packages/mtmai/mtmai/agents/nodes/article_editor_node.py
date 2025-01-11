from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState, tools_condition

from mtmai.agents.graphchatdemo.tools.search_tools import search_tool
from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()



class ArticleEditorNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        thread_ui_state = state.thread_ui_state
        return {
            "thread_ui_state": {
                "playData": {
                        "title": "Hello World2222",
                        "content": "This is a test post",
                },
            },
        }
