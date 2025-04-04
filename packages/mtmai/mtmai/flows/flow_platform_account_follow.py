from clients.rest.models.flow_platform_account_follow_input import (
    FlowPlatformAccountFollowInput,
)
from loguru import logger
from mtmai.agents._types import IgLoginRequire
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_error import FlowError
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.platform_account_upsert import PlatformAccountUpsert
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.flows.flow_ctx import FlowCtx
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtlibs.instagrapi.exceptions import BadPassword, TwoFactorRequired
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.PLATFORM_ACCOUNT_FOLLOW,
    on_events=[f"{FlowNames.PLATFORM_ACCOUNT_FOLLOW}"],
)
class FlowPlatformAccountFollow:
    @mtmapp.step(timeout="5m")
    async def entry(self, hatctx: Context):
        """
        Instagram账号的关注
        """
        from mtmai.mtlibs.instagrapi import Client

        flowctx = FlowCtx().from_hatctx(hatctx)
        input = FlowPlatformAccountFollowInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        # STEP1: 获取登录状态
        result = await tenant_client.platform_account_api.platform_account_get(
            tenant=tid,
            platform_account=input.platform_account_id,
        )
        ig_client = Client(proxy=result.state.get("proxy_url"))
        try:
            login_result = ig_client.login(
                username=input.username,
                password=input.password,
                verification_code=input.two_factor_code,
                relogin=False,
            )
            if not login_result:
                raise Exception("登录失败")
            platform_account_id = generate_uuid()
            result = await tenant_client.platform_account_api.platform_account_upsert(
                tenant=tid,
                platform_account=platform_account_id,
                platform_account_upsert=PlatformAccountUpsert(
                    username=input.username,
                    password=input.password,
                    state=ig_client.get_settings(),
                ),
            )
            return {"result": "todo", "id": result.metadata.id}
        except TwoFactorRequired as e:
            logger.error(f"需要二次验证: {e}")
            # tenant_client.platform_account_api.platform_account_upsert(
            #     tenant=tid,
            #     platform_account=input.platform_account_id,
            #     platform_account_upsert=PlatformAccountUpsert(
            #         username=input.username,
            #         password=input.password,
            #         error=str(e),
            #     ),
            # )
            raise e
        except BadPassword:
            # tenant_client.platform_account_api.platform_account_update(
            #     tenant=tid,
            #     platform_account=input.platform_account_id,
            #     platform_account_update=PlatformAccountUpdate(
            #         # status=PlatformAccountStatus.FAILED,
            #     ),
            # )
            return IgLoginRequire(
                username=input.username,
                password=input.password,
            )
        except Exception as e:
            return FlowError(
                error=str(e),
            ).model_dump()
