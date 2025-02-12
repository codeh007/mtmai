from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from mtmai.agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest.models.team_component import TeamComponent
from mtmai.agents.team_builder.company_research import CompanyResearchTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from autogen_core import RoutedAgent, message_handler, type_subscription, default_subscription


# @default_subscription
@type_subscription(topic_type="tenant")
class TenantAgent(RoutedAgent):
    def __init__(self, ctx: AgentContext) -> None:
        super().__init__("TenantAgent")
        self.apictx = ctx

    @message_handler
    async def handle_tenant_message_type(self, message: TenantSeedReq, mctx: MessageContext) -> None:
        # self.apictx.log(f"{self.id.type} received message: {message.content}")
        if not message.tenant_id or len(message.tenant_id) == 0:
            raise ValueError("tenantId 不能为空")
        self.apictx.log(f"当前租户: {message.tenant_id}")
        # 获取模型配置
        self.apictx.log("获取模型配置")
        defaultModel = await self.apictx.aio.model_api.model_get(
            tenant=message.tenant_id, model="default"
        )
        self.apictx.log(defaultModel)

        model_config = defaultModel.config
        team_builder = TravelTeamBuilder()
        team1 = await team_builder.create_travel_agent(model_config)
        team2 = await CompanyResearchTeamBuilder().create_company_research_team(
            model_config
        )

        all_teams = [team1, team2]
        for team in all_teams:
            # 保存 team
            team_comp = team.dump_component()
            comp = TeamComponent(**team_comp.model_dump())
            team2 = Team(
                    label=team_comp.label,
                    description=team_comp.description or "",
                    component=comp,
                )
            defaultModel = await self.apictx.aio.team_api.team_upsert(
                tenant=message.tenant_id,
                team=team._team_id,
                team2=team2,
            )
            self.apictx.log(defaultModel)

    # @message_handler
    # async def on_text_message(self, message: MyTextMessage, ctx: MessageContext) -> None:
    #     logger.info(f"Hello, {message.source}, you said {message.content}!")

    # @message_handler
    # async def on_image_message(self, message: MyImageMessage, ctx: MessageContext) -> None:
    #     logger.info(f"Hello, {message.source}, you sent me {message.url}!")
