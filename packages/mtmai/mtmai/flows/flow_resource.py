from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.resource_flow_input import ResourceFlowInput
from mtmai.clients.rest.models.state_type import StateType
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.RESOURCE,
    on_events=[f"{FlowNames.RESOURCE}"],
)
class FlowResource:
    @mtmapp.step(timeout="60m")
    async def entry(self, hatctx: Context):
        input = ResourceFlowInput.model_validate(hatctx.input)
        tenant_client = TenantClient()
        cancellation_token = MtCancelToken()
        session_id = get_chat_session_id_ctx()
        if not session_id:
            session_id = "default"

        resource_data = await tenant_client.resource_api.resource_get(
            tenant=tenant_client.tenant_id,
            resource=input.resource_id,
        )
        logger.info(f"resource_data: {resource_data}")

        resource_type = resource_data.type

        if resource_type == "platform_account":
            # logger.info(f"resource_type: {resource_type}")
            team = await tenant_client.load_team("instagram_team")

            result = await team.run_stream(
                task=input, cancellation_token=cancellation_token
            )
            # 保存团队状态
            for k, v in result.items():
                logger.info(f"key: {k}, value: {v}")
                parts = k.split("/")
                topic = parts[0]
                source = parts[1] if len(parts) > 1 else "default"
                await tenant_client.ag_state_api.ag_state_upsert(
                    tenant=tenant_client.tenant_id,
                    ag_state_upsert=AgStateUpsert(
                        tenantId=tenant_client.tenant_id,
                        topic=topic,
                        source=source,
                        type=StateType.RUNTIMESTATE.value,
                        componentId=input.component_id,
                        chatId=session_id,
                        state=v,
                    ),
                )
        else:
            logger.error(f"unknown resource_type: {resource_type}")
        return {"output": "Hello, FlowResource!"}
