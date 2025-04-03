from clients.rest.models.platform_account_update import PlatformAccountUpdate
from flows.flow_ctx import FlowCtx
from loguru import logger
from mtlibs.instagrapi.exceptions import BadPassword, TwoFactorRequired
from mtmai.agents._types import IgLoginRequire
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.platform_account_flow_input import (
    PlatformAccountFlowInput,
)
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.PLATFORM_ACCOUNT,
    on_events=[f"{FlowNames.PLATFORM_ACCOUNT}"],
)
class FlowPlatformAccount:
    @mtmapp.step(timeout="5m")
    async def entry(self, hatctx: Context):
        """
        社交媒体账号的初始化
        """
        flowctx = FlowCtx().from_hatctx(hatctx)
        input = PlatformAccountFlowInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        platform_account_data = (
            await tenant_client.platform_account_api.platform_account_get(
                tenant=tid,
                platform_account=input.platform_account_id,
            )
        )
        logger.info(f"platform_account_data: {platform_account_data}")

        # STEP1: 登录
        try:
            from mtmai.mtlibs.instagrapi import Client

            ig_client = Client()
            login_result = ig_client.login(
                platform_account_data.username, platform_account_data.password
            )
            # ig_client.dump_settings(IG_CREDENTIAL_PATH)
            ig_client.login(
                platform_account_data.username, platform_account_data.password
            )
        except TwoFactorRequired as e:
            logger.error(f"需要二次验证: {e}")
            raise e
        except BadPassword:
            tenant_client.platform_account_api.platform_account_update(
                tenant=tid,
                platform_account=input.platform_account_id,
                platform_account_update=PlatformAccountUpdate(
                    # status=PlatformAccountStatus.FAILED,
                ),
            )
            return IgLoginRequire(
                username=platform_account_data.username,
                password=platform_account_data.password,
            )
        except Exception as e:
            logger.error(f"登录失败: {e}")
            raise e
        return {"result": "todo"}
