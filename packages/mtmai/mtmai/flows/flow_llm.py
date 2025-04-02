from fastapi.encoders import jsonable_encoder
from loguru import logger
from model_client.model_client import MtOpenAIChatCompletionClient
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.run_flow_model_input import RunFlowModelInput
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="model",
    on_events=["model"],
)
class FlowModel:
    @mtmapp.step(timeout="10m")
    async def entry(self, hatctx: Context):
        input = RunFlowModelInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        if not input.model_id:
            models = await tenant_client.ag.model_api.model_list(tenant=tid)
            if not models.rows:
                raise ValueError("No model found")
            modelObj = models.rows[0]
        else:
            modelObj = await tenant_client.ag.model_api.model_get(
                model_id=input.model_id
            )
        model_client = MtOpenAIChatCompletionClient.load_component(modelObj)
        create_result = await model_client.create(
            messages=[
                {"role": "user", "content": "Hello, how are you?"},
            ]
        )
        logger.info(create_result)
        return jsonable_encoder(create_result)
