from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import BaseTool

from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState
logger = get_logger()

class ShowAdminPanelTool(BaseTool):
    name: str = "ShowAdminPanelTool"
    description: str = (
        r"当用户明确要求显示管理面板、后台面板时,显示管理面板给用户进行下一步的操作"
    )
    response_format: str = "content_and_artifact"

    def _run(self):
        return (
            "Operation successful",
            {
                "artiface_type": "AdminView",
                "title": "管理面板",
                "props": {
                    "title": "管理面板",
                },
            },
        )


class ShowTasksInputPanelTool(BaseTool):
    name: str = "ShowTasksInputPanel"
    description: str = (
        r"有用的工具, 向用户UI 显示任务输入的选择器, 让用户选择需要运行的任务"
    )
    response_format: str = "content_and_artifact"

    def _run(self):
        return (
            "Operation successful",
            {
                "artiface_type": "TaskSelect",
                "title": "任务选择器",
                "props": {
                    "title": "任务选择器",
                },
            },
        )


show_admin_panel_tool = ShowAdminPanelTool()
form_tool = ShowTasksInputPanelTool()
human_node_tools = [
    show_admin_panel_tool,
    form_tool,
]


class HumanNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        logger.info("进入 human_node")
        messages = state.messages
        user_input = state.user_input
        # if user_input:
        #     messages.append(HumanMessage(content=user_input))

        if user_input == "/1":
            logger.info("特殊指令1")

        return {
            "messages": HumanMessage(content=user_input),
        }
