from clients.rest.models.flow_names import FlowNames
from clients.rest.models.run_flow_model_input import RunFlowModelInput
from clients.rest.models.tenant_setting_content import TenantSettingContent
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp
from teams.tenant_team import TenantTeam


@mtmapp.workflow(
    name=FlowNames.TENANT,
    on_events=[FlowNames.TENANT],
)
class FlowTenant:
    @mtmapp.step(timeout="3m")
    async def entry(self, hatctx: Context):
        input = RunFlowModelInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        # TODO: 从服务器获取
        tenant_setting = TenantSettingContent(
            enabled_instagram_task=True,
        )

        # gallery_builder = builder.create_default_gallery_builder()
        # tenant_team_component = gallery_builder.get_team("Tenant Team")
        # tenant_team = Team.load_component(tenant_team_component)

        tenant_team = TenantTeam()
        result2 = await tenant_team.run(hatctx)
        if tenant_setting.enabled_instagram_task:
            pass
        return {
            "success": True,
            "tenant_id": tid,
            "message": "tenant success",
        }
