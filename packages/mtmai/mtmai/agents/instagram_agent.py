import email
import imaplib
import random
import re
from typing import Any, AsyncGenerator, List, Mapping, Sequence

import pyotp
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from autogen_core import CancellationToken, MessageContext, RoutedAgent, message_handler
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ChatCompletionClient
from loguru import logger
from mtmai.clients.rest.models.instagram_agent_state import InstagramAgentState
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.core.config import settings
from mtmai.mtlibs.instagrapi import Client
from mtmai.mtlibs.instagrapi.mixins.challenge import ChallengeChoice
from mtmai.mtlibs.instagrapi.types import Media


class InstagramAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        user_topic: str,
        model_client: ChatCompletionClient | None = None,
    ) -> None:
        super().__init__(
            description=description or "An agent that interacts with instagram",
        )
        self.model_client = model_client
        self.user_topic = user_topic
        self._model_context = BufferedChatCompletionContext(buffer_size=10)
        self._initialized = False
        self.ig_client = Client()
        self._state = InstagramAgentState(
            proxy=settings.default_proxy_url,
        )
        self.tenant_client = TenantClient()

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
        return login_result

    @message_handler
    async def handle_add_follow(
        self, message: SocialAddFollowersInput, ctx: MessageContext
    ) -> None:
        if not self._state.ig_settings:
            raise Exception("ig 未登录")
        logger.info(f"(instagram agent )SocialAddFollowersInput  with {ctx.sender}")

    async def on_messages_stream(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
        async for message in super().on_messages_stream(messages, cancellation_token):
            yield message

    async def example(self):
        # IG_CREDENTIAL_PATH = "./ig_settings.json"
        # SLEEP_TIME = "600"  # in seconds

        self.ig_client.login(self.username, self.password)
        # self.ig_client.dump_settings(IG_CREDENTIAL_PATH)

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

    # async def run(self, hatctx: Context, input: SocialAddFollowersInput):
    #     await self._init()
    #     try:
    #         state_from_db = await self.tenant_client.flow_state_api.flow_state_get(
    #             tenant=self.tenant_client.tenant_id,
    #             session=self.tenant_client.session_id,
    #             workflow=hatctx.action.job_id,
    #         )
    #     except Exception as e:
    #         logger.debug(f"Error getting flow state: {e}")
    #         state_from_db = None

    #     if state_from_db:
    #         self._state = InstagramAgentState.from_dict(state_from_db.state)
    #     else:
    #         self._state = InstagramAgentState(
    #             proxy=settings.default_proxy_url,
    #         )
    #     self.ig_client = Client(
    #         proxy=self._state.proxy_url or settings.default_proxy_url,
    #     )
    #     if self._state.ig_settings:
    #         self.ig_client.set_settings(
    #             self._state.ig_settings,
    #         )

    #     if isinstance(input.actual_instance, SocialLoginInput):
    #         return await self.on_social_login(hatctx, input.actual_instance)
    #     elif isinstance(input.actual_instance, SocialAddFollowersInput):
    #         return await hatctx.aio.spawn_workflow(FlowNames.INSTAGRAM, input)
    #     else:
    #         raise ValueError("(FlowInstagram)Invalid input type")

    # def get_client(self):
    #     """We return the client class, in which we automatically handle exceptions
    #     You can move the "handle_exception" above or into an external module
    #     """

    #     def handle_exception(client, e):
    #         if isinstance(e, BadPassword):
    #             client.logger.exception(e)
    #             client.set_proxy(self.next_proxy().href)
    #             if client.relogin_attempt > 0:
    #                 self.freeze(str(e), days=7)
    #                 raise ReloginAttemptExceeded(e)
    #             client.settings = self.rebuild_client_settings()
    #             return self.update_client_settings(client.get_settings())
    #         elif isinstance(e, LoginRequired):
    #             client.logger.exception(e)
    #             client.relogin()
    #             return self.update_client_settings(client.get_settings())
    #         elif isinstance(e, ChallengeRequired):
    #             api_path = client.last_json.get("challenge", {}).get("api_path")
    #             if api_path == "/challenge/":
    #                 client.set_proxy(self.next_proxy().href)
    #                 client.settings = self.rebuild_client_settings()
    #             else:
    #                 try:
    #                     client.challenge_resolve(client.last_json)
    #                 except ChallengeRequired as e:
    #                     self.freeze("Manual Challenge Required", days=2)
    #                     raise e
    #                 except (
    #                     ChallengeRequired,
    #                     SelectContactPointRecoveryForm,
    #                     RecaptchaChallengeForm,
    #                 ) as e:
    #                     self.freeze(str(e), days=4)
    #                     raise e
    #                 self.update_client_settings(client.get_settings())
    #             return True
    #         elif isinstance(e, FeedbackRequired):
    #             message = client.last_json["feedback_message"]
    #             if "This action was blocked. Please try again later" in message:
    #                 self.freeze(message, hours=12)
    #                 # client.settings = self.rebuild_client_settings()
    #                 # return self.update_client_settings(client.get_settings())
    #             elif "We restrict certain activity to protect our community" in message:
    #                 # 6 hours is not enough
    #                 self.freeze(message, hours=12)
    #             elif "Your account has been temporarily blocked" in message:
    #                 """
    #                 Based on previous use of this feature, your account has been temporarily
    #                 blocked from taking this action.
    #                 This block will expire on 2020-03-27.
    #                 """
    #                 self.freeze(message)
    #         elif isinstance(e, PleaseWaitFewMinutes):
    #             self.freeze(str(e), hours=1)
    #         raise e

    #     cl = Client()
    #     cl.handle_exception = handle_exception
    #     cl.login(self.username, self.password)

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

    # @classmethod
    # def _from_config(cls, config: InstagramAgentConfig) -> Self:
    #     return cls(
    #         name=config.name,
    #         model_client=ChatCompletionClient.load_component(
    #             config.model_client.model_dump()
    #         ),
    #         tools=[BaseTool.load_component(tool) for tool in config.tools]
    #         if config.tools
    #         else None,
    #         model_context=None,
    #         memory=[Memory.load_component(memory) for memory in config.memory]
    #         if config.memory
    #         else None,
    #         description=config.description,
    #         system_message=config.system_message,
    #         model_client_stream=config.model_client_stream,
    #         reflect_on_tool_use=config.reflect_on_tool_use,
    #         tool_call_summary_format=config.tool_call_summary_format,
    #         handoffs=config.handoffs,
    #         username=config.username,
    #         password=config.password,
    #     )

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass

    async def save_state(self) -> Mapping[str, Any]:
        model_context_state = await self._model_context.save_state()
        return InstagramAgentState(
            llm_context=model_context_state,
            username=self._state.username,
            password=self._state.password,
            otp_key=self._state.otp_key,
            proxy_url=self._state.proxy_url,
            ig_settings=self.ig_client.get_settings(),
        ).model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        self._state = InstagramAgentState.from_dict(state)
        self.ig_client.set_settings(self._state.ig_settings)
        self.ig_client.set_proxy(self._state.proxy_url)

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
