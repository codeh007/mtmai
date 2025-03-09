from loguru import logger
from mtmai.agents.team_builder.instagram_team_builder import InstagramTeamBuilder
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context_client import TenantClient


def percentage_change_tool(start: float, end: float) -> float:
    return ((end - start) / start) * 100


class ResourceTeamBuilder:
    """资源管理团队"""

    @property
    def name(self):
        return "resource_team"

    @property
    def description(self):
        return "resource_team"

    async def create_team(self, message: AgentRunInput):
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        model_client = await tenant_client.ag.default_model_client(
            tenant_client.tenant_id
        )
        resource_data = await tenant_client.ag.resource_api.resource_get(
            tenant=tid,
            resource=message.resource_id,
        )
        # platform_account_data = PlatformAccountData.model_validate(
        #     platform_account.content
        # )
        logger.info(f"resource_data: {resource_data}")
        # return team
        if resource_data.type == "platform_account":
            return await InstagramTeamBuilder().create_team(model_client)
        raise ValueError(
            f"cant create team for unsupported resource type: {resource_data.type}"
        )
