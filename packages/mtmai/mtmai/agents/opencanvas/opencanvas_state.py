from enum import Enum
from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class Highlight(BaseModel):
    id: str
    startCharIndex: int
    endCharIndex: int


class Artifact(BaseModel):
    id: str
    content: str
    title: str
    type: Literal["code", "text"]
    language: str


class LanguageOptions(str, Enum):
    english = "english"
    mandarin = "mandarin"
    spanish = "spanish"
    french = "french"
    hindi = "hindi"


class UiState(BaseModel):
    showWorkbench: bool | None = None
    currentWorkbenchView: str | None = None


class OpenCanvasState(BaseModel):
    messages: Annotated[list, add_messages] = []
    uiState: UiState = UiState()
    selectedArtifactId: str | None = None
    highlighted: Highlight | None = None
    next: str | None = None
    siteId: str | None = None
    userId: str | None = None
    params: dict | None = None
    #   * The artifacts that wave been generated in the conversation.
    artifacts: Annotated[list[Artifact], add_messages] = []
    # The language to translate the artifact to.
    language: LanguageOptions | None = None
