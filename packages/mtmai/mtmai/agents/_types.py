from abc import ABC, abstractmethod
from typing import List

from autogen_core.models import LLMMessage
from mtmai.clients.rest.models.browser_open_task import BrowserOpenTask
from mtmai.clients.rest.models.browser_task import BrowserTask
from mtmai.clients.rest.models.code_review_result import CodeReviewResult
from mtmai.clients.rest.models.code_review_task import CodeReviewTask
from mtmai.clients.rest.models.code_writing_result import CodeWritingResult
from mtmai.clients.rest.models.code_writing_task import CodeWritingTask
from mtmai.clients.rest.models.platform_account_task import PlatformAccountTask
from mtmai.clients.rest.models.team_runner_task import TeamRunnerTask
from mtmai.clients.rest.models.termination_message import TerminationMessage
from pydantic import BaseModel


class UserTask(BaseModel):
    context: List[LLMMessage]


class AgentResponse(BaseModel):
    reply_to_topic_type: str
    context: List[LLMMessage]


class IntentClassifierBase(ABC):
    @abstractmethod
    async def classify_intent(self, message: str) -> str:
        pass


class AgentRegistryBase(ABC):
    @abstractmethod
    async def get_agent(self, intent: str) -> str:
        pass


class UserTextMessage(BaseModel):
    source: str
    content: str


class AssistantTextMessage(BaseModel):
    source: str
    content: str


class GetSlowUserMessage(BaseModel):
    content: str


class TerminateMessage(BaseModel):
    content: str


class ScheduleMeetingOutput(BaseModel):
    pass


agent_message_types = [
    TerminationMessage,
    CodeWritingTask,
    CodeWritingResult,
    CodeReviewTask,
    CodeReviewResult,
    TeamRunnerTask,
    PlatformAccountTask,
    BrowserOpenTask,
    BrowserTask,
    #
    ScheduleMeetingOutput,
    GetSlowUserMessage,
    AssistantTextMessage,
    UserTextMessage,
]
