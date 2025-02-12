from typing import Annotated, Literal, Optional

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class UiState(BaseModel):
    showWorkbench: bool | None = None
    currentWorkbenchView: str | None = None


class Topic(BaseModel):
    topic: str = Field(description="The topic for the post")


class ArticleArtifact(BaseModel):
    id: str
    content: str
    title: str
    type: Literal["code", "text"]
    language: str


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class MtmState(BaseModel):
    messages: Annotated[list, add_messages] = []
    uiState: UiState = UiState()
    # scheduleId: str | None = None
    # taskId: str | None = None
    next: str | None = None
    # userId: str | None = None
    artifacts: list[ArticleArtifact] = []
    user_input: str | None = None

    # human 节点直接输出给前端用户的消息
    human_ouput_message: str | None = None
    is_debug: bool | None = False
    task_config: dict | None = None

    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "update_flight",
                "book_car_rental",
                "book_hotel",
                "book_excursion",
            ]
        ],
        update_dialog_stack,
    ]
