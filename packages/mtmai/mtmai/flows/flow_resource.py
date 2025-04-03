from loguru import logger
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.resource_flow_input import ResourceFlowInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.flows.flow_ctx import FlowCtx
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.RESOURCE,
    on_events=[f"{FlowNames.RESOURCE}"],
)
class FlowResource:
    @mtmapp.step(timeout="60m")
    async def entry(self, hatctx: Context):
        flowctx = FlowCtx().from_hatctx(hatctx)
        input = ResourceFlowInput.model_validate(hatctx.input)
        tenant_client = TenantClient()

        resource_data = await tenant_client.resource_api.resource_get(
            tenant=tenant_client.tenant_id,
            resource=input.resource_id,
        )
        logger.info(f"resource_data: {resource_data}")

        resource_type = resource_data.type

        if resource_type == "platform_account":
            logger.info(f"resource_type: {resource_type}")
        else:
            logger.error(f"unknown resource_type: {resource_type}")
        return {"output": "Hello, FlowResource!"}
