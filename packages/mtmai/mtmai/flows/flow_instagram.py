from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_instagram_input import FlowInstagramInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.instagram_agent_state import InstagramAgentState
from mtmai.clients.rest.models.social_add_followers_input import SocialAddFollowersInput
from mtmai.clients.rest.models.social_login_input import SocialLoginInput
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.mtlibs.instagrapi import Client
from mtmai.worker_app import mtmapp

default_proxy_url = "http://127.0.0.1:10809"


@mtmapp.workflow(
    name=FlowNames.INSTAGRAM,
    on_events=[f"{FlowNames.INSTAGRAM}"],
)
class FlowInstagram:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = FlowInstagramInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        self._state = InstagramAgentState(
            proxy=default_proxy_url,
        )
        self.ig_client = Client(
            proxy=default_proxy_url,
        )

        if isinstance(input.actual_instance, SocialLoginInput):
            return await self.on_social_login(hatctx, input.actual_instance)
        elif isinstance(input.actual_instance, SocialAddFollowersInput):
            return await hatctx.aio.spawn_workflow(FlowNames.INSTAGRAM, input)
        else:
            raise ValueError("(FlowInstagram)Invalid input type")

    async def on_social_login(self, hatctx: Context, msg: SocialLoginInput):
        logger.info(f"input: {msg}")
        return {"state": "social_login"}

    async def on_social_add_followers(
        self, hatctx: Context, msg: SocialAddFollowersInput
    ):
        logger.info(f"input: {msg}")
        return {"state": "social_add_followers"}

    async def load_state(self, hatctx: Context):
        return {"state": "load_state"}
