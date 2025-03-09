from abc import ABC, abstractmethod
from typing import Dict, List

from autogen_agentchat.base import TaskResult
from autogen_core.models import LLMMessage
from mtmai.clients.rest.models.code_writing_task import CodeWritingTask
from mtmai.clients.rest.models.platform_account_task import PlatformAccountTask
from pydantic import BaseModel


# Define WriterAgent configuration model
class ChatAgentConfig(BaseModel):
    topic_type: str
    description: str
    system_message: str


# Define UI Agent configuration model
class UIAgentConfig(BaseModel):
    topic_type: str
    artificial_stream_delay_seconds: Dict[str, float]

    @property
    def min_delay(self) -> float:
        return self.artificial_stream_delay_seconds.get("min", 0.0)

    @property
    def max_delay(self) -> float:
        return self.artificial_stream_delay_seconds.get("max", 0.0)


class ApiSaveTeamState(BaseModel):
    tenant_id: str
    # team_id: str
    state: dict
    componentId: str
    runId: str


class ApiSaveTeamTaskResult(BaseModel):
    tenant_id: str
    team_id: str
    task_result: TaskResult


class SetupHfSpaceMsg(BaseModel):
    tenant_id: str
    username: str
    password: str


class LogItemMsg(BaseModel):
    content: str


# class MsgStartWebServer(BaseModel):
#     pass


class MsgGetTeam(BaseModel):
    tenant_id: str
    team_id: str


class UserTask(BaseModel):
    context: List[LLMMessage]


class AgentResponse(BaseModel):
    reply_to_topic_type: str
    context: List[LLMMessage]


class TerminationMessage(BaseModel):
    """A message that is sent from the system to the user, indicating that the conversation has ended."""

    reason: str


# class CodeWritingTask(BaseModel):
#     task: str


class CodeWritingResult(BaseModel):
    task: str
    code: str
    review: str


class CodeReviewTask(BaseModel):
    session_id: str
    code_writing_task: str
    code_writing_scratchpad: str
    code: str


class CodeReviewResult(BaseModel):
    review: str
    session_id: str
    approved: bool


class TeamRunnerTask(BaseModel):
    task: str
    team: str


# browser


class BrowserOpenTask(BaseModel):
    """打开浏览器备用,一般用于调试目的Open a browser and navigate to a URL."""

    url: str


class BrowserTask(BaseModel):
    task: str


class IntentClassifierBase(ABC):
    @abstractmethod
    async def classify_intent(self, message: str) -> str:
        pass


class AgentRegistryBase(ABC):
    @abstractmethod
    async def get_agent(self, intent: str) -> str:
        pass


# @dataclass(kw_only=True)
# class BaseMessage:
#     """A basic message that stores the source of the message."""

#     source: str


agent_message_types = [
    TerminationMessage,
    CodeWritingTask,
    CodeWritingResult,
    CodeReviewTask,
    CodeReviewResult,
    TeamRunnerTask,
    PlatformAccountTask,
]
