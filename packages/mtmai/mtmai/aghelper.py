import logging

from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest_client import AsyncRestApi

from .agents.model_client import MtmOpenAIChatCompletionClient
from .mtlibs.id import generate_uuid
from .team_builder.assisant_team_builder import AssistantTeamBuilder

logger = logging.getLogger(__name__)


class AgHelper:
    def __init__(self, gomtmapi: AsyncRestApi) -> None:
        self.gomtmapi = gomtmapi

    async def get_or_create_default_team(self, tenant_id: str, label: str):
        teams_list = await self.gomtmapi.teams_api.team_list(
            tenant=tenant_id, label=label
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            return teams_list.rows[0]
        else:
            logger.info(f"create default team for tenant {tenant_id}")
            defaultModel = await self.gomtmapi.model_api.model_get(
                tenant=tenant_id, model="default"
            )
            model_dict = defaultModel.config.model_dump()
            model_dict.pop("n", None)
            # model_dict["model_info"] = model_dict.pop("model_info", None)
            model_client = MtmOpenAIChatCompletionClient(
                **model_dict,
            )

            default_team_builder = AssistantTeamBuilder()
            team_comp = await default_team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            comp = component_model.model_dump()
            team2 = Team(
                label=component_model.label,
                description=component_model.description or "",
                component=comp,
            )
            logger.info(f"create default team for tenant {tenant_id}")
            new_team = await self.gomtmapi.team_api.team_upsert(
                tenant=tenant_id,
                team=generate_uuid(),
                team2=team2,
            )
            return new_team
