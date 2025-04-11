import email
import imaplib
import random
import re
from typing import Any, Awaitable, Callable, Dict, List, Mapping, Sequence

import pyotp
from autogen_agentchat.base import Handoff as HandoffBase
from autogen_core import (
    CancellationToken,
    Component,
    DefaultTopicId,
    MessageContext,
    message_handler,
)
from autogen_core.memory import Memory
from autogen_core.model_context import ChatCompletionContext
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import BaseTool
from loguru import logger
from mtlibs.autogen_utils.component_loader import ComponentLoader
from mtmai.agents.assistant_agent import AssistantAgent
from mtmai.clients.rest.models.agent_state_types import AgentStateTypes
from mtmai.clients.rest.models.agent_topic_types import AgentTopicTypes
from mtmai.clients.rest.models.flow_login_result import FlowLoginResult
from mtmai.clients.rest.models.instagram_agent_config import InstagramAgentConfig
from mtmai.clients.rest.models.instagram_agent_state import InstagramAgentState
from mtmai.clients.rest.models.instagram_credentials import InstagramCredentials
from mtmai.clients.rest.models.platform_account_upsert import PlatformAccountUpsert
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.context.context import Context
from mtmai.core.config import settings
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtlibs.instagrapi import Client
from mtmai.mtlibs.instagrapi.mixins.challenge import ChallengeChoice
from mtmai.mtlibs.instagrapi.types import Media
from pydantic import BaseModel
from typing_extensions import Self


class InstagramAgent(AssistantAgent, Component[InstagramAgentConfig]):
    component_type = "agent"
    component_provider_override = "mtmai.agents.instagram_agent.InstagramAgent"
    component_config_schema = InstagramAgentConfig

    def __init__(
        self,
        name: str,
        model_client: ChatCompletionClient,
        *,
        credentials: InstagramCredentials,
        tools: List[
            BaseTool[Any, Any] | Callable[..., Any] | Callable[..., Awaitable[Any]]
        ]
        | None = None,
        handoffs: List[HandoffBase | str] | None = None,
        model_context: ChatCompletionContext | None = None,
        description: str = "An agent that interacts with instagram",
        system_message: (
            str | None
        ) = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed.",
        model_client_stream: bool = False,
        reflect_on_tool_use: bool | None = None,
        tool_call_summary_format: str = "{result}",
        output_content_type: type[BaseModel] | None = None,
        memory: Sequence[Memory] | None = None,
        metadata: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            model_client=model_client,
            tools=tools or [],
            handoffs=handoffs,
            model_context=model_context,
            description=description or self.DEFAULT_DESCRIPTION,
            system_message=system_message or self.DEFAULT_SYSTEM_MESSAGE,
            model_client_stream=model_client_stream,
            reflect_on_tool_use=reflect_on_tool_use,
            tool_call_summary_format=tool_call_summary_format,
            output_content_type=output_content_type,
            memory=memory,
            metadata=metadata,
        )
        # self.user_topic = user_topic
        self._state = InstagramAgentState(
            type=AgentStateTypes.INSTAGRAMAGENTSTATE.value,
        )
        self._credentials = credentials

    @message_handler
    async def on_instagram_login(
        self, message: SocialLoginInput, ctx: MessageContext
    ) -> bool:
        # await self._init()
        login_result = self.ig_client.login(
            username=message.username,
            password=message.password,
            verification_code=pyotp.TOTP(message.otp_key).now(),
            relogin=False,
        )
        if not login_result:
            raise Exception("ig 登录失败")
        self._state.ig_settings = self.ig_client.get_settings()
        self._state.proxy_url = settings.default_proxy_url
        self._state.username = message.username
        self._state.password = message.password
        self._state.otp_key = message.otp_key

        platform_account = (
            await self.tenant_client.platform_account_api.platform_account_upsert(
                tenant=self.tenant_client.tenant_id,
                platform_account=generate_uuid(),
                platform_account_upsert=PlatformAccountUpsert(
                    label="platform_account",
                    description="platform_account",
                    platform="instagram",
                    enable=True,
                    username=message.username,
                    password=message.password,
                    state={
                        "otp_key": message.otp_key,
                        "proxy_url": settings.default_proxy_url,
                    },
                ),
            )
        )
        # 发布结果
        await self.publish_message(
            FlowLoginResult(
                type="FlowLoginResult",
                content="登录成功",
                source=self.id.key,
                success=True,
                account_id=platform_account.metadata.id,
            ),
            topic_id=DefaultTopicId(
                type=AgentTopicTypes.RESPONSE.value, source=ctx.topic_id.source
            ),
        )
        return login_result

    @message_handler
    async def handle_add_follow(
        self, message: SocialAddFollowersInput, ctx: MessageContext
    ) -> None:
        if not self._state.ig_settings:
            raise Exception("ig 未登录")
        logger.info(f"(instagram agent )SocialAddFollowersInput  with {ctx.sender}")

    # async def on_messages_stream(
    #     self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    # ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
    #     async for message in super().on_messages_stream(messages, cancellation_token):
    #         yield message

    async def example(self):
        # IG_CREDENTIAL_PATH = "./ig_settings.json"
        # SLEEP_TIME = "600"  # in seconds
        self.ig_client.login(self.username, self.password)
        userid = self.ig_client.user_id_from_username("hello")
        self.ig_client.user_follow(userid)
        self.ig_client.user_unfollow(userid)
        self.ig_client.user_followers(userid, amount=10)
        self.ig_client.user_following(userid, amount=10)
        self.ig_client.user_followers_full(userid, amount=10)

    async def get_code_from_email(username):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        CHALLENGE_EMAIL = ""
        CHALLENGE_PASSWORD = ""
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

    async def on_social_login(self, hatctx: Context, msg: SocialLoginInput):
        logger.info(f"input: {msg}")
        self._state.username = msg.username
        self._state.password = msg.password
        self._state.otp_key = msg.otp_key

        return {"state": "social_login"}

    async def on_social_add_followers(
        self, hatctx: Context, msg: SocialAddFollowersInput
    ):
        logger.info(f"input: {msg}")
        return {"state": "social_add_followers"}

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        await super().on_reset(cancellation_token)
        self._state = InstagramAgentState(
            type=AgentStateTypes.INSTAGRAMAGENTSTATE.value,
        )

    async def save_state(self) -> Mapping[str, Any]:
        self._state.llm_context = await self._model_context.save_state()
        return self._state.model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = InstagramAgentState.from_dict(state)
        self.ig_client.set_settings(self._state.ig_settings)
        self.ig_client.set_proxy(self._state.proxy_url)

    async def _to_config(self) -> InstagramAgentConfig:
        if self._output_content_type:
            raise ValueError(
                "AssistantAgent with output_content_type does not support declarative config."
            )

        return InstagramAgentConfig(
            name=self.name,
            model_client=self._model_client.dump_component(),
            tools=[tool.dump_component() for tool in self._tools],
            handoffs=list(self._handoffs.values()) if self._handoffs else None,
            model_context=self._model_context.dump_component(),
            memory=[memory.dump_component() for memory in self._memory]
            if self._memory
            else None,
            description=self.description,
            system_message=self._system_messages[0].content
            if self._system_messages
            and isinstance(self._system_messages[0].content, str)
            else None,
            model_client_stream=self._model_client_stream,
            reflect_on_tool_use=self._reflect_on_tool_use,
            tool_call_summary_format=self._tool_call_summary_format,
            metadata=self._metadata,
            credentials=self._credentials,
        )

    @classmethod
    def _from_config(cls, config: InstagramAgentConfig) -> Self:
        return cls(
            name=config.name,
            model_client=ComponentLoader.load_component(
                config.model_client, ChatCompletionClient
            ),
            tools=[
                ComponentLoader.load_component(tool, expected=BaseTool)
                for tool in config.tools
            ]
            if config.tools
            else None,
            model_context=None,
            memory=[
                ComponentLoader.load_component(memory, expected=Memory)
                for memory in config.memory
            ]
            if config.memory
            else None,
            description=config.description,
            system_message=config.system_message,
            model_client_stream=config.model_client_stream,
            reflect_on_tool_use=config.reflect_on_tool_use,
            tool_call_summary_format=config.tool_call_summary_format,
            handoffs=config.handoffs,
            credentials=config.credentials,
        )
