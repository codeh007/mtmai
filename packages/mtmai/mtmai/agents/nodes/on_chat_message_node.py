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


def edge_chat_node(state: HomeChatState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "chat_tools_node"
    if state.get("next"):
        return state.get("next")
    else:
        return "continue"


@tool(parse_docstring=False, response_format="content_and_artifact")
def open_document_editor(title: str, state: Annotated[dict, InjectedState]):
    """Useful to show document editor ui for user, 用户能够看到这个编辑器进行文章编辑"""
    return (
        "操作成功",
        {
            "artifaceType": "Document",
            "props": {
                "id": "fake-document-id",
                "title": "document-title1",
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def create_document(title: str, content: str, state: Annotated[dict, InjectedState]):
    """Useful to create new document for user"""
    return (
        "操作成功",
        {
            "artifaceType": "Document",
            "props": {
                "id": "fake-document-id",
                "title": title,
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def show_workflow_image():
    """Useful tool for displaying the internal workflow diagram of the current agent."""
    return (
        "Operation successful",
        {
            "artifaceType": "Image",
            "props": {
                "src": f"{settings.API_V1_STR}/agent/image/mtmaibot",
                "title": "流程图",
            },
        },
    )


@tool(parse_docstring=False, response_format="content_and_artifact")
def show_supperadmin_panel():
    """当用户明确要求显示管理面板时，显示管理面板给用户进行下一步的操作"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


chatbot_tools = [
    search_tool,
    create_document,
]


class OnChatMessageNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        messages = state.messages
        user_input = state.user_input
        if user_input:
            messages.append(HumanMessage(content=user_input))
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是网站前端 copilot 助手，负责展示网站前端管理面板，用户通过管理面板可以进行文章编辑，文章发布等操作，引导用户使用本系统"
                    "[ IMPORTANT ]:"
                    "优先用文字回复用户，除非涉及到UI操作，比如文章编辑，发布等才调用工具。",
                    "\n- 必须使用简体中文",
                ),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )
        messages = await direct_gen_outline_prompt.ainvoke({"messages": messages})
        ai_msg = await self.runnable.ainvoke(messages, config)

        return {
            "messages": [
                ai_msg,
            ],
        }
