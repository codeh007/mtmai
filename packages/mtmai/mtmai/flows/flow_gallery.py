from clients.rest.models.flow_names import FlowNames
from clients.rest.models.mt_component import MtComponent
from clients.rest.models.run_flow_model_input import RunFlowModelInput
from mtlibs.id import generate_uuid
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.GALLERY,
    on_events=[FlowNames.GALLERY],
)
class FlowGallery:
    @mtmapp.step(timeout="5m")
    async def entry(self, hatctx: Context):
        from gallery.builder import create_default_gallery_builder

        input = RunFlowModelInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        gallery_builder = create_default_gallery_builder()

        for team in gallery_builder.teams:
            component_id = generate_uuid()
            mt_component = MtComponent(
                componentType=team.component_type,
                # componentId=component_id,
                componentVersion=1,
                provider=team.provider,
                label=team.name,
                description=team.description,
                config=team.config,
            )
            await tenant_client.ag.coms_api.coms_upsert(
                tenant=tid,
                com=component_id,
                mt_component=mt_component,
            )

        return {
            "success": True,
        }
