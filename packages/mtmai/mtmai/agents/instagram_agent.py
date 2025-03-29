import email
import imaplib
import random
import re
from typing import Any, Awaitable, Callable, Dict, List, Sequence

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents._assistant_agent import AssistantAgentConfig
from autogen_agentchat.base import Handoff as HandoffBase
from autogen_agentchat.base import Response
from autogen_agentchat.messages import ChatMessage, TextMessage
from autogen_core import CancellationToken, Component, MessageContext, message_handler
from autogen_core.memory import Memory
from autogen_core.model_context import ChatCompletionContext
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import BaseTool
from autogen_ext.tools.mcp import mcp_server_tools
from context.context_client import TenantClient
from loguru import logger
from model_client.utils import get_default_model_client
from mtlibs.mcp import print_mcp_tools
from mtmai.clients.rest.models.agent_config import AgentConfig

# from mtmai.clients.rest.models.instagram_agent_config import InstagramAgentConfig
from mtmai.mtlibs.instagrapi import Client
from mtmai.mtlibs.instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
)
from mtmai.mtlibs.instagrapi.mixins.challenge import ChallengeChoice
from mtmai.mtlibs.instagrapi.types import Media
from pydantic import BaseModel
from typing_extensions import Self

CHALLENGE_EMAIL = ""
CHALLENGE_PASSWORD = ""


class IgAccountMessage(BaseModel):
    username: str | None = None
    password: str | None = None


class InstagramAgentConfig(AssistantAgentConfig):
    username: str | None = None
    password: str | None = None


class InstagramAgent(AssistantAgent, Component[InstagramAgentConfig]):
    component_config_schema = InstagramAgentConfig
    component_provider_override = "mtmai.agents.instagram_agent.InstagramAgent"

    def __init__(
        self,
        name: str,
        model_client: ChatCompletionClient,
        *,
        tools: List[
            BaseTool[Any, Any] | Callable[..., Any] | Callable[..., Awaitable[Any]]
        ]
        | None = None,
        handoffs: List[HandoffBase | str] | None = None,
        model_context: ChatCompletionContext | None = None,
        description: str = "An agent that provides assistance with ability to use tools.",
        system_message: (
            str | None
        ) = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed.",
        model_client_stream: bool = False,
        reflect_on_tool_use: bool = False,
        tool_call_summary_format: str = "{result}",
        memory: Sequence[Memory] | None = None,
        metadata: Dict[str, str] | None = None,
    ) -> None:
        name = "InstagramAgent"

        model_client = get_default_model_client()
        tenant_client = TenantClient()
        server_params = tenant_client.get_mcp_endpoint()

        # Get all available tools from the server
        super().__init__(
            name=name,
            model_client=model_client,
            tools=tools,
            handoffs=handoffs,
            model_context=model_context,
            description=description,
            system_message=system_message,
            model_client_stream=model_client_stream,
            reflect_on_tool_use=reflect_on_tool_use,
            tool_call_summary_format=tool_call_summary_format,
            memory=memory,
        )

    @message_handler
    async def handle_ig_account(
        self, message: IgAccountMessage, ctx: MessageContext
    ) -> None:
        """初始化社交账号"""
        logger.info(f"handle_ig_account: {message}")
        # human_input = input("Human agent input: ")
        # human_input = await self.get_user_input("Human agent input: ")
        # logger.info("TODO: need human input")
        # logger.info(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
        # message.context.append(
        #     AssistantMessage(content=human_input, source=self.id.type)
        # )
        # await self.publish_message(
        #     AgentResponse(
        #         context=message.context, reply_to_topic_type=self._agent_topic_type
        #     ),
        #     topic_id=TopicId(self._user_topic_type, source=self.id.key),
        # )

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                return message
        raise AssertionError("The stream should have returned the final result.")

    async def example(self):
        IG_USERNAME = ""
        IG_PASSWORD = ""
        IG_CREDENTIAL_PATH = "./ig_settings.json"
        # SLEEP_TIME = "600"  # in seconds

        ig_client = Client()
        ig_client.login(IG_USERNAME, IG_PASSWORD)
        ig_client.dump_settings(IG_CREDENTIAL_PATH)

        userid = ig_client.user_id_from_username("hello")
        ig_client.user_follow(userid)
        ig_client.user_unfollow(userid)
        ig_client.user_followers(userid, amount=10)
        ig_client.user_following(userid, amount=10)
        ig_client.user_followers_full(userid, amount=10)

    async def get_code_from_email(username):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
        mail.select("inbox")
        result, data = mail.search(None, "(UNSEEN)")
        assert result == "OK", "Error1 during get_code_from_email: %s" % result
        ids = data.pop().split()
        for num in reversed(ids):
            mail.store(num, "+FLAGS", "\\Seen")  # mark as read
            result, data = mail.fetch(num, "(RFC822)")
            assert result == "OK", "Error2 during get_code_from_email: %s" % result
            msg = email.message_from_string(data[0][1].decode())
            payloads = msg.get_payload()
            if not isinstance(payloads, list):
                payloads = [msg]
            code = None
            for payload in payloads:
                body = payload.get_payload(decode=True).decode()
                if "<div" not in body:
                    continue
                match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
                if not match:
                    continue
                print("Match from email:", match.group(1))
                match = re.search(r">(\d{6})<", body)
                if not match:
                    print('Skip this email, "code" not found')
                    continue
                code = match.group(1)
                if code:
                    return code
        return False

    def get_code_from_sms(username):
        while True:
            code = input(f"Enter code (6 digits) for {username}: ").strip()
            if code and code.isdigit():
                return code
        return None

    def challenge_code_handler(self, username, choice):
        if choice == ChallengeChoice.SMS:
            return self.get_code_from_sms(username)
        elif choice == ChallengeChoice.EMAIL:
            return self.get_code_from_email(username)
        return False

    def change_password_handler(username):
        # Simple way to generate a random string
        chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
        password = "".join(random.sample(chars, 10))
        return password

    def download_all_medias(self, username: str, amount: int = 5) -> dict:
        """
        Download all medias from instagram profile
        """
        amount = int(amount)
        cl = Client()
        cl.login(self._username, self._password)
        user_id = cl.user_id_from_username(username)
        medias = cl.user_medias(user_id)
        result = {}
        i = 0
        for m in medias:
            if i >= amount:
                break
            paths = []
            if m.media_type == 1:
                # Photo
                paths.append(cl.photo_download(m.pk))
            elif m.media_type == 2 and m.product_type == "feed":
                # Video
                paths.append(cl.video_download(m.pk))
            elif m.media_type == 2 and m.product_type == "igtv":
                # IGTV
                paths.append(cl.video_download(m.pk))
            elif m.media_type == 2 and m.product_type == "clips":
                # Reels
                paths.append(cl.video_download(m.pk))
            elif m.media_type == 8:
                # Album
                for path in cl.album_download(m.pk):
                    paths.append(path)
            result[m.pk] = paths
            print(f"http://instagram.com/p/{m.code}/", paths)
            i += 1
        return result

    def get_client(self):
        """We return the client class, in which we automatically handle exceptions
        You can move the "handle_exception" above or into an external module
        """

        def handle_exception(client, e):
            if isinstance(e, BadPassword):
                client.logger.exception(e)
                client.set_proxy(self.next_proxy().href)
                if client.relogin_attempt > 0:
                    self.freeze(str(e), days=7)
                    raise ReloginAttemptExceeded(e)
                client.settings = self.rebuild_client_settings()
                return self.update_client_settings(client.get_settings())
            elif isinstance(e, LoginRequired):
                client.logger.exception(e)
                client.relogin()
                return self.update_client_settings(client.get_settings())
            elif isinstance(e, ChallengeRequired):
                api_path = client.last_json.get("challenge", {}).get("api_path")
                if api_path == "/challenge/":
                    client.set_proxy(self.next_proxy().href)
                    client.settings = self.rebuild_client_settings()
                else:
                    try:
                        client.challenge_resolve(client.last_json)
                    except ChallengeRequired as e:
                        self.freeze("Manual Challenge Required", days=2)
                        raise e
                    except (
                        ChallengeRequired,
                        SelectContactPointRecoveryForm,
                        RecaptchaChallengeForm,
                    ) as e:
                        self.freeze(str(e), days=4)
                        raise e
                    self.update_client_settings(client.get_settings())
                return True
            elif isinstance(e, FeedbackRequired):
                message = client.last_json["feedback_message"]
                if "This action was blocked. Please try again later" in message:
                    self.freeze(message, hours=12)
                    # client.settings = self.rebuild_client_settings()
                    # return self.update_client_settings(client.get_settings())
                elif "We restrict certain activity to protect our community" in message:
                    # 6 hours is not enough
                    self.freeze(message, hours=12)
                elif "Your account has been temporarily blocked" in message:
                    """
                    Based on previous use of this feature, your account has been temporarily
                    blocked from taking this action.
                    This block will expire on 2020-03-27.
                    """
                    self.freeze(message)
            elif isinstance(e, PleaseWaitFewMinutes):
                self.freeze(str(e), hours=1)
            raise e

        cl = Client()
        cl.handle_exception = handle_exception
        cl.login(self.username, self.password)

    async def filter_medias(
        medias: List[Media],
        like_count_min=None,
        like_count_max=None,
        comment_count_min=None,
        comment_count_max=None,
        days_ago_max=None,
    ):
        from datetime import datetime, timedelta

        medias = list(
            filter(
                lambda x: True
                if like_count_min is None
                else x.like_count >= like_count_min,
                medias,
            )
        )
        medias = list(
            filter(
                lambda x: True
                if like_count_max is None
                else x.like_count <= like_count_max,
                medias,
            )
        )
        medias = list(
            filter(
                lambda x: True
                if comment_count_min is None
                else x.comment_count >= comment_count_min,
                medias,
            )
        )
        medias = list(
            filter(
                lambda x: True
                if comment_count_max is None
                else x.comment_count <= comment_count_max,
                medias,
            )
        )
        if days_ago_max is not None:
            days_back = datetime.now() - timedelta(days=days_ago_max)
            medias = list(
                filter(
                    lambda x: days_ago_max is None
                    or x.taken_at is None
                    or x.taken_at > days_back.astimezone(x.taken_at.tzinfo),
                    medias,
                )
            )

        return list(medias)

    def next_proxy():
        """
        例子:
        # cl = Client(proxy=next_proxy())
        # try:
        #     cl.login("USERNAME", "PASSWORD")
        # except (ProxyError, HTTPError, GenericRequestError, ClientConnectionError):
        #     # Network level
        #     cl.set_proxy(next_proxy())
        # except (SentryBlock, RateLimitError, ClientThrottledError):
        #     # Instagram limit level
        #     cl.set_proxy(next_proxy())
        # except (ClientLoginRequired, PleaseWaitFewMinutes, ClientForbiddenError):
        #     # Logical level
        #     cl.set_proxy(next_proxy())
        """

        return random.choice(
            [
                "http://username:password@147.123123.123:412345",
                "http://username:password@147.123123.123:412346",
                "http://username:password@147.123123.123:412347",
            ]
        )

    @classmethod
    def _from_config(cls, config: AgentConfig | InstagramAgentConfig) -> Self:
        """Create an assistant agent from a declarative config."""
        _config = config
        if isinstance(config, AgentConfig):
            # _config=config.
            return cls(
                name=config.name,
                model_client=ChatCompletionClient.load_component(config.model_client),
                tools=[BaseTool.load_component(tool) for tool in config.tools]
                if config.tools
                else None,
                handoffs=config.handoffs,
                model_context=None,
                memory=[Memory.load_component(memory) for memory in config.memory]
                if config.memory
                else None,
                description=config.description,
            )
        else:
            return cls(
                name=config.name,
                model_client=ChatCompletionClient.load_component(
                    config.model_client.model_dump()
                ),
                tools=[BaseTool.load_component(tool) for tool in config.tools]
                if config.tools
                else None,
                handoffs=config.handoffs,
                model_context=None,
                memory=[Memory.load_component(memory) for memory in config.memory]
                if config.memory
                else None,
                description=config.description,
                system_message=config.system_message,
                model_client_stream=config.model_client_stream,
                reflect_on_tool_use=config.reflect_on_tool_use,
                tool_call_summary_format=config.tool_call_summary_format,
            )

    @classmethod
    async def from_context(cls) -> Self:
        tenant_client = TenantClient()
        model_client = get_default_model_client()

        server_params = await tenant_client.get_mcp_endpoint()
        tools = await mcp_server_tools(server_params)
        print_mcp_tools(tools)

        return cls(
            name="InstagramAgent",
            model_client=model_client,
            tools=tools,
            handoffs=[],
            model_context=None,
            memory=[],
            description="An agent that provides assistance with ability to use tools.",
            # system_message=config.system_message,
            # model_client_stream=config.model_client_stream,
            # reflect_on_tool_use=config.reflect_on_tool_use,
            # tool_call_summary_format=config.tool_call_summary_format,
        )

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)
        pass
