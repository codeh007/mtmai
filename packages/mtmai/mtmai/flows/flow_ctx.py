from autogen_agentchat.base import Team
from loguru import logger
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.gallery import builder
from mtmai.mtlibs.id import is_uuid
from mtmai.teams.social.instagram_team import InstagramTeam, InstagramTeamConfig
from typing_extensions import Self


class FlowCtx:
    def __init__(self):
        self.tenant_client = TenantClient()
        self.session_id = get_chat_session_id_ctx()
        # self.tid = get_tenant_id()

    # 看起来过时了,原因是, autogen 中的team 的行为本身就可以立即为一个agent,
    # 因此,后续的设计以 agent 自身作为主导,而不是team
    async def load_team(self, team_comp_id_or_name: str):
        if is_uuid(team_comp_id_or_name):
            # 从数据库加载
            try:
                component_data = await self.tenant_client.ag.coms_api.coms_get(
                    tenant=self.tenant_client.tenant_id,
                    com=team_comp_id_or_name,
                )
                logger.info(f"component data: {component_data}")
            except Exception as e:
                logger.exception(f"获取组件数据失败: {e}")
                raise e

            if component_data.component_type == ComponentTypes.TEAM:
                comp_dict = component_data.model_dump()
                team = Team.load_component(comp_dict)
                self.team = team
            else:
                raise ValueError(f"组件类型错误: {component_data.component_type}")

        elif team_comp_id_or_name == "instagram_team":
            team = InstagramTeam._from_config(InstagramTeamConfig())
            return team
            # gallery_builder = builder.create_default_gallery_builder()
            # tenant_team_component = gallery_builder.get_team("instagram_team")
            # tenant_team = Team.load_component(tenant_team_component)
            # return tenant_team
        else:
            gallery_builder = builder.create_default_gallery_builder()
            tenant_team_component = gallery_builder.get_team("Tenant Team")
            tenant_team = Team.load_component(tenant_team_component)
            return tenant_team

        return team

    @classmethod
    def from_hatctx(cls, hatctx: Context) -> Self:
        ctx = cls()
        ctx.hatctx = hatctx
        return ctx
