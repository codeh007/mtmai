from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from pydantic import BaseModel

from mtmai.models.task import MtTask


class UiState(BaseModel):
    showWorkbench: bool | None = None
    currentWorkbenchView: str | None = None


class ArticleArtifact(BaseModel):
    id: str
    content: str
    title: str
    type: Literal["code", "text"]
    language: str


class TaskState(BaseModel):
    messages: Annotated[list, add_messages] = []
    uiState: UiState = UiState()
    scheduleId: str | None = None
    taskId: str | None = None
    next: str | None = None
    userId: str | None = None
    artifacts: list[ArticleArtifact] = []
    task_data: MtTask | None = None
    user_input: str | None = None

    # human 节点直接输出给前端用户的消息
    human_ouput_message: str | None = None
    is_debug: bool | None = False
    task_config: dict | None = None
