from datetime import datetime

from clients.rest.models.flow_names import FlowNames
from clients.rest.models.mt_component import MtComponent
from clients.rest.models.run_flow_model_input import RunFlowModelInput
from mtlibs.id import generate_uuid
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp
from mtmpb.mtm_pb2 import APIResourceMeta


@mtmapp.workflow(
    name=FlowNames.GALLERY,
    on_events=[FlowNames.GALLERY],
)
class FlowGallery:
    @mtmapp.step(timeout="3m")
    async def entry(self, hatctx: Context):
        from mtmai.gallery.builder import create_default_gallery_builder

        input = RunFlowModelInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        gallery_builder = create_default_gallery_builder()

        gallery_id = generate_uuid()
        for component in (
            gallery_builder.teams
            + gallery_builder.agents
            + gallery_builder.models
            + gallery_builder.tools
            + gallery_builder.terminations
        ):
            component_id = generate_uuid()
            component.component_version
            mt_component = MtComponent(
                metadata=APIResourceMeta(
                    id=component_id,
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                ),
                gallery_id=gallery_id,
                componentType=component.component_type,
                provider=component.provider,
                label=component.label,
                description=component.description,
                version=component.version,
                componentVersion=component.component_version,
                config=component.config,
            )
            await tenant_client.ag.coms_api.coms_upsert(
                tenant=tid,
                com=component_id,
                mt_component=mt_component,
            )

        return {
            "success": True,
        }
