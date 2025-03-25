import os
from typing import Dict, List

from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.mtlibs.instagrapi import Client
from mtmai.mtlibs.instagrapi.types import UserShort
from mtmai.worker_app import mtmapp

IG_USERNAME = ""
IG_PASSWORD = ""
IG_CREDENTIAL_PATH = "./ig_settings.json"
SLEEP_TIME = "600"  # in seconds


@mtmapp.workflow(
    name="ig",
    on_events=["ig"],
)
class FlowIG:
    _cl = None

    def __init__(self):
        pass

    def follow_by_username(self, username) -> bool:
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_follow(userid)

    def unfollow_by_username(self, username) -> bool:
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_unfollow(userid)

    def get_followers(self, amount: int = 0) -> Dict[int, UserShort]:
        return self._cl.user_followers(self._cl.user_id, amount=amount)

    def get_followers_usernames(self, amount: int = 0) -> List[str]:
        followers = self._cl.user_followers(self._cl.user_id, amount=amount)
        return [user.username for user in followers.values()]

    def get_following(self, amount: int = 0) -> Dict[int, UserShort]:
        return self._cl.user_following(self._cl.user_id, amount=amount)

    def get_following_usernames(self, amount: int = 0) -> List[str]:
        following = self._cl.user_following(self._cl.user_id, amount=amount)
        return [user.username for user in following.values()]

    @mtmapp.step(timeout="60m")
    async def entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        ig_client = Client()

        if os.path.exists(IG_CREDENTIAL_PATH):
            ig_client.load_settings(IG_CREDENTIAL_PATH)
            ig_client.login(IG_USERNAME, IG_PASSWORD)
        else:
            ig_client.login(IG_USERNAME, IG_PASSWORD)
            ig_client.dump_settings(IG_CREDENTIAL_PATH)

        return {
            "status": "browser ok, success",
        }
