from autogen_core import MessageContext, RoutedAgent, message_handler
from loguru import logger
from mtmai.agents._types import PlatformAccountTask
from mtmai.clients.rest.models.platform_account_data import PlatformAccountData
from mtmai.context.context_client import TenantClient


class PlatformAccountAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
    ) -> None:
        super().__init__(description)

    @message_handler
    async def handle_task(
        self, message: PlatformAccountTask, ctx: MessageContext
    ) -> None:
        logger.info(f"Platform account agent received task: {message}")
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        platform_account = await tenant_client.ag.resource_api.resource_get(
            tenant=tid,
            resource=message.id,
        )
        platform_account_data = PlatformAccountData.model_validate(
            platform_account.content
        )
        logger.info(f"platform_account_data: {platform_account_data}")
