import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    import mtmai


class AgentTaskBase(SQLModel):
    title: str | None = Field(default="")


class AgentTask(AgentTaskBase, table=True):
    """对应 langgraph 一个工作流的运行"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )

    # id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    # user_id: str = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    output: str | None = Field(default="")
    config: RunnableConfig = Field(sa_column=Column(JSON))


class AgentMeta(BaseModel):
    id: str
    name: str
    base_url: str
    chat_url: str | None = None
    can_chat: bool = (False,)
    agent_type: str | None = None
    graph_image: str | None = None
    label: str | None = None
    description: str | None = None


class CopilotScreen(SQLModel):
    id: str
    label: str | None = None
    Icon: str | None = None


# ui 状态相关开始
class ChatBotUiStateBase(SQLModel):
    class Config:
        arbitrary_types_allowed = True

    agent: str | None = None
    layout: str | None = None
    theme: str | None = None
    # config: dict = Field(default_factory=dict, sa_column=Column(JSON))
    isOpen: bool = Field(default=False)
    fabDisplayText: str | None = Field(default=None)
    fabDisplayIcon: str | None = Field(default=None)
    fabDisplayColor: str | None = Field(default=None)
    fabDisplayAction: str | None = Field(default=None)
    isOpenDataView: bool = Field(default=False)
    activateViewName: str | None = None
    activateChatProfileId: str | None = None
    screens: list[CopilotScreen] = Field(default_factory=list)  # 过时，


class ChatBotUiStateResponse(ChatBotUiStateBase):
    pass


class ChatBotUiState(ChatBotUiStateBase):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="uimessages")


class ArtifaceBase(SQLModel):
    artiface_type: str
    title: str | None = None
    description: str | None = None
    props: dict = Field(default_factory=dict, sa_column=Column(JSON))


class AgentViewType(str, Enum):
    SIDEBAR = "sidebar"  # IDE 右侧聊天样式
    POPUP = "popup"  # 页面中央弹出式


class AgentBootstrap(SQLModel):
    """前端获取 agent 的配置
    前端全局agent 加载器会在所有页面加载时返回配置初始化agent UI
    """

    # 前端agent 视图类型
    view_type: AgentViewType | None = Field(default=AgentViewType.SIDEBAR)
    # 是否显示浮动按钮
    is_show_fab: bool = Field(default=True)

    # 其他配置以后再补充


class ChatbotBase(SQLModel):
    title: str | None = Field(default="")
    description: str | None = Field(default="")
    config: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Chatbot(ChatbotBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    # messages: list["UiMessage"] = Relationship(back_populates="chatbot")


class UiMessageBase(SQLModel):
    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True

    role: str | None = Field(default=None, max_length=64)
    content: str | None = Field(default=None)
    component: str | None = Field(default=None, max_length=64)  # 可能过时了。
    props: dict | None = Field(default=None, sa_column=Column(JSON))  # 可能过时了。
    artifacts: list[dict] | None = Field(default=None, sa_column=Column(JSON))


class UiMessage(UiMessageBase, table=True):
    """前端 聊天机器人的消息列表组件"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    chatbot_id: str = Field(default=None, foreign_key="chatbot.id")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
