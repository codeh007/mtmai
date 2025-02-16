from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from pydantic import BaseModel, Field

from mtmai.models.chat import ThreadUIState


class LlmItem(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: str
    name: str
    provider: str | None = None
    llm_type: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    is_tool_use: bool | None = None
    temperature: float = 0.7
    model: str | None = None
    max_tokens: int = 8000


class HomeChatState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages]
    user_input: str | None = None
    user_info: str | None = None
    error: str | None = None
    thread_ui_state: ThreadUIState = Field(default=None)
    next: str | None = None  # 下一跳 （过时, 改用 dialog_state）
    dialog_state: str | None = (
        None  # 当前处理用户对话的节点 名 (因为特定的功能节点本身可以直接跟用户对话)
    )


class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Content of the subsection")

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.description}".strip()


class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    description: str = Field(..., title="Content of the section")
    subsections: list[Subsection] | None = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Wikipedia page.",
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            f"### {subsection.subsection_title}\n\n{subsection.description}"
            for subsection in self.subsections or []
        )
        return f"## {self.section_title}\n\n{self.description}\n\n{subsections}".strip()


class Outline(BaseModel):
    page_title: str = Field(..., title="Title of the Wikipedia page")
    sections: list[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the Wikipedia page.",
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{sections}".strip()


def add_messages(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def update_references(references, new_references):
    if not references:
        references = {}
    references.update(new_references)
    return references


def update_editor(editor, new_editor):
    # Can only set at the outset
    if not editor:
        return new_editor
    return editor


# Generate Perspectives
class Editor(BaseModel):
    affiliation: str = Field(
        description="Primary affiliation of the editor.",
    )
    name: str = Field(
        description="Name of the editor.", pattern=r"^[a-zA-Z0-9_-]{1,64}$"
    )
    role: str = Field(
        description="Role of the editor in the context of the topic.",
    )
    description: str = Field(
        description="Description of the editor's focus, concerns, and motives.",
    )

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"


class Perspectives(BaseModel):
    editors: list[Editor] = Field(
        description="Comprehensive list of editors with their roles and affiliations.",
        # Add a pydantic validation/restriction to be at most M editors
    )


class InterviewState(BaseModel):
    messages: list[AnyMessage] = []
    references: dict | None = None
    editor: Editor | None = None


class WikiSection(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    content: str = Field(..., title="Full content of the section")
    subsections: list[Subsection] | None = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Wikipedia page.",
    )
    citations: list[str] = Field(default_factory=list)

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            subsection.as_str for subsection in self.subsections or []
        )
        citations = "\n".join([f" [{i}] {cit}" for i, cit in enumerate(self.citations)])
        return (
            f"## {self.section_title}\n\n{self.content}\n\n{subsections}".strip()
            + f"\n\n{citations}".strip()
        )


class ResearchState(BaseModel):
    error: str | None = None
    topic: str | None = None
    outline: Outline | None = None
    editors: list[Editor] | None = None
    interview_results: list[InterviewState] | None = None
    # The final sections output
    sections: list[WikiSection] | None = None
    article: str | None = None
    # context: Annotated[AgentContext, Context(make_agent_context)]


class MtmaiTool(BaseModel):
    """
    工具定义:
        一般用于根据名称动态获取工具函数的场景
    """

    name: str
    # 敏感工具调用前，自动停止等待用户确认
    is_sensitive: bool | None = False


class Assistant(BaseModel):
    id: str
    name: str
    goal: str | None = None
    # 背景信息
    background_prompt: str | None = None
    additional_prompt: str | None = None
    tools: list[MtmaiTool] | None = None

    # 下级助理
    # 用于完成特定任务，可以直接回复用户
    # 用户应该感觉不到二级助理的存在
    # 如果对话记录超过二级助理的职能范围，自动以 pop 的方式退回到上级助理
    children: list["Assistant"] | None = None

    # 明确的入口参数，告知上级助理如果需要进入该助理时，需要传递的参数
    entry_params: dict | None = None
    depth: int | None = 0


class GraphConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    llms: list[LlmItem]
    # 链调用失败是自动重试的次数
    llm_retry_default: int = 3
    assistants: list[Assistant]
