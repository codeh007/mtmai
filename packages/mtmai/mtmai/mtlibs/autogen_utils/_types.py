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
    SocialLoginInput,
    SocialAddFollowersInput,
    FlowLoginResult,
    FlowResult,
    FlowHandoffResult,
]
