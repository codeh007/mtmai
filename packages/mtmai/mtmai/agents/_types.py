from abc import ABC, abstractmethod
from typing import List

from autogen_core.models import LLMMessage
from mtmai.clients.rest.models.browser_open_task import BrowserOpenTask
from mtmai.clients.rest.models.browser_task import BrowserTask
from mtmai.clients.rest.models.code_review_result import CodeReviewResult
from mtmai.clients.rest.models.code_review_task import CodeReviewTask
from mtmai.clients.rest.models.code_writing_result import CodeWritingResult
from mtmai.clients.rest.models.code_writing_task import CodeWritingTask
from mtmai.clients.rest.models.flow_handoff_result import FlowHandoffResult
from mtmai.clients.rest.models.flow_login_result import FlowLoginResult
from mtmai.clients.rest.models.flow_result import FlowResult
from mtmai.clients.rest.models.platform_account_task import PlatformAccountTask
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.rest.models.team_runner_task import TeamRunnerTask
from mtmai.clients.rest.models.termination_message import TerminationMessage
from pydantic import BaseModel

# sales_agent_topic_type = "SalesAgent"
# issues_and_repairs_agent_topic_type = "IssuesAndRepairsAgent"
# triage_agent_topic_type = "TriageAgent"
# reviewer_agent_topic_type = "ReviewerAgent"
# team_runner_topic_type = "TeamRunner"
# platform_account_topic_type = "PlatformAccount"
# scheduling_assistant_topic_type = "scheduling_assistant_conversation"


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


# class ScheduleMeetingOutput(BaseModel):
#     pass


# class IgLoginRequire(BaseModel):
#     username: str | None = None
#     password: str | None = None
#     twofa_code: str | None = None


# class IgAccountMessage(BaseModel):
#     username: str | None = None
#     password: str | None = None
#     twofa_code: str | None = None


# class InstagramLoginMessage(TextMessage):
#     username: str | None = None
#     password: str | None = None


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
    GetSlowUserMessage,
    AssistantTextMessage,
    UserTextMessage,
    # IgLoginRequire,
    # IgAccountMessage,
    SocialLoginInput,
    SocialAddFollowersInput,
    FlowLoginResult,
    FlowResult,
    FlowHandoffResult,
]
