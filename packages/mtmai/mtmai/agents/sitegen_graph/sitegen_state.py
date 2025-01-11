from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class UiState(BaseModel):
    showWorkbench: bool | None = None
    currentWorkbenchView: str | None = None


class ArticleArtifact(BaseModel):
    id: str
    content: str
    title: str
    type: Literal["code", "text"]
    language: str


class AssistantState(BaseModel):
    messages: Annotated[list, add_messages] = []
    uiState: UiState = UiState()
    selectedArtifactId: str | None = None
    # highlighted: Highlight | None = None
    next: str | None = None
    siteId: str | None = None
    userId: str | None = None
    params: dict | None = None
    #   * The artifacts that wave been generated in the conversation.
    artifacts: Annotated[list[ArticleArtifact], add_messages] = []
    # The language to translate the artifact to.
    # language: LanguageOptions | None = None
