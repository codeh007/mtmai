from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.mt_component_upsert import MtComponentUpsert
from mtmai.clients.rest.models.run_flow_model_input import RunFlowModelInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.gallery.builder import create_default_gallery_builder
from mtmai.mtlibs.id import generate_uuid
from mtmai.worker_app import mtmapp


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
        gallery_builder = create_default_gallery_builder()
        gallery_id = generate_uuid()
        for component in gallery_builder.teams:
            mt_component_upsert = MtComponentUpsert(
                galleryId=gallery_id,
                label=component.label,
                description=component.description,
                version=component.version,
                component_version=component.component_version,
                provider=component.provider,
                component_type=component.component_type,
                config=component.config,
            )
            await tenant_client.coms_api.coms_upsert(
                tenant=tid,
                com=generate_uuid(),
                mt_component_upsert=mt_component_upsert.model_dump(),
            )
        return {
            "success": True,
        }
